from pymongo import MongoClient

client = MongoClient()

db = client.controller

# Collections
"""Agent registration"""
collection_agents = db["agents"]

"""Device Sync"""
collection_sync_device = db["sync"]