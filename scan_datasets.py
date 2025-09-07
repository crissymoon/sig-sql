import os
import asyncio
import aiofiles
from pathlib import Path
from typing import Generator, Dict, List, Optional, Union
from concurrent.futures import ThreadPoolExecutor
import mimetypes
import json
import pandas as pd

def scan_dataset_folder(folder_path: str, 
                       include_formats: Optional[List[str]] = None,
                       exclude_formats: Optional[List[str]] = None,
                       max_workers: int = 4,
                       include_metadata: bool = True) -> Generator[Dict, None, None]:
    
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Dataset folder not found: {folder_path}")
    
    supported_formats = {
        '.csv', '.json', '.xlsx', '.xls', '.parquet', '.pkl', '.pickle',
        '.tsv', '.txt', '.xml', '.yaml', '.yml', '.h5', '.hdf5',
        '.feather', '.orc', '.avro', '.jsonl', '.ndjson'
    }
    
    if include_formats:
        target_formats = set(f".{fmt.lstrip('.')}" for fmt in include_formats)
    else:
        target_formats = supported_formats
    
    if exclude_formats:
        exclude_set = set(f".{fmt.lstrip('.')}" for fmt in exclude_formats)
        target_formats = target_formats - exclude_set
    
    folder_path_obj = Path(folder_path)
    
    for file_path in folder_path_obj.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in target_formats:
            file_info = {
                'file_path': str(file_path),
                'file_name': file_path.name,
                'file_extension': file_path.suffix.lower(),
                'file_size_bytes': file_path.stat().st_size,
                'relative_path': str(file_path.relative_to(folder_path_obj))
            }
            
            if include_metadata:
                try:
                    file_info.update(_get_file_metadata(file_path))
                except Exception as e:
                    file_info['metadata_error'] = str(e)
            
            yield file_info

def _get_file_metadata(file_path: Path) -> Dict:
    metadata = {}
    file_ext = file_path.suffix.lower()
    
    try:
        if file_ext == '.csv':
            df_sample = pd.read_csv(file_path, nrows=1)
            metadata['columns'] = list(df_sample.columns)
            metadata['estimated_rows'] = sum(1 for _ in open(file_path)) - 1
            
        elif file_ext == '.json':
            with open(file_path, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    metadata['type'] = 'array'
                    metadata['length'] = len(data)
                    if data:
                        metadata['sample_keys'] = list(data[0].keys()) if isinstance(data[0], dict) else None
                elif isinstance(data, dict):
                    metadata['type'] = 'object'
                    metadata['keys'] = list(data.keys())
                    
        elif file_ext in ['.xlsx', '.xls']:
            xl_file = pd.ExcelFile(file_path)
            metadata['sheet_names'] = xl_file.sheet_names
            metadata['sheet_count'] = len(xl_file.sheet_names)
            
        elif file_ext == '.parquet':
            df_sample = pd.read_parquet(file_path)
            metadata['columns'] = list(df_sample.columns)
            metadata['shape'] = df_sample.shape
            metadata['dtypes'] = df_sample.dtypes.to_dict()
            
        elif file_ext in ['.pkl', '.pickle']:
            metadata['type'] = 'pickle'
            metadata['readable'] = True
            
    except Exception as e:
        metadata['parse_error'] = str(e)
    
    return metadata

async def scan_dataset_folder_async(folder_path: str,
                                   include_formats: Optional[List[str]] = None,
                                   exclude_formats: Optional[List[str]] = None,
                                   max_workers: int = 4) -> List[Dict]:
    
    loop = asyncio.get_event_loop()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        files = await loop.run_in_executor(
            executor,
            lambda: list(scan_dataset_folder(folder_path, include_formats, exclude_formats, max_workers, True))
        )
    
    return files

def get_dataset_summary(folder_path: str) -> Dict:
    files = list(scan_dataset_folder(folder_path))
    
    summary = {
        'total_files': len(files),
        'total_size_bytes': sum(f['file_size_bytes'] for f in files),
        'file_types': {},
        'largest_file': None,
        'folder_structure': set()
    }
    
    for file_info in files:
        ext = file_info['file_extension']
        summary['file_types'][ext] = summary['file_types'].get(ext, 0) + 1
        
        if not summary['largest_file'] or file_info['file_size_bytes'] > summary['largest_file']['file_size_bytes']:
            summary['largest_file'] = file_info
        
        folder = str(Path(file_info['relative_path']).parent)
        summary['folder_structure'].add(folder)
    
    summary['folder_structure'] = sorted(list(summary['folder_structure']))
    summary['total_size_mb'] = round(summary['total_size_bytes'] / (1024 * 1024), 2)
    
    return summary

def filter_files_by_criteria(folder_path: str,
                            min_size_bytes: Optional[int] = None,
                            max_size_bytes: Optional[int] = None,
                            contains_columns: Optional[List[str]] = None) -> List[Dict]:
    
    filtered_files = []
    
    for file_info in scan_dataset_folder(folder_path):
        if min_size_bytes and file_info['file_size_bytes'] < min_size_bytes:
            continue
        if max_size_bytes and file_info['file_size_bytes'] > max_size_bytes:
            continue
        if contains_columns and 'columns' in file_info:
            if not all(col in file_info['columns'] for col in contains_columns):
                continue
        
        filtered_files.append(file_info)
    
    return filtered_files