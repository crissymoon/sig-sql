import os
import sys
from django.conf import settings
from django.db import models
from django.utils import timezone
import json

# Remove the problematic import - we'll handle this in views.py instead

class ChatSession(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_activity = models.DateTimeField(auto_now=True)
    learning_weights = models.JSONField(default=dict)
    total_interactions = models.IntegerField(default=0)
    avg_satisfaction = models.FloatField(default=0.0)

class ChatInteraction(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    user_input = models.TextField()
    data_content = models.TextField()
    storage_recommendation = models.CharField(max_length=100)
    confidence_score = models.FloatField()
    features_analyzed = models.JSONField()
    processing_time = models.FloatField()
    user_feedback = models.FloatField(null=True, blank=True)
    success = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

class LearningPattern(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, null=True, blank=True)
    context_type = models.CharField(max_length=50, default='general')
    storage_choice = models.CharField(max_length=100, default='hybrid_intelligent')
    feedback_score = models.FloatField(null=True, blank=True)
    success = models.BooleanField(null=True, blank=True)
    weights_before = models.JSONField(default=dict)
    weights_after = models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now)
