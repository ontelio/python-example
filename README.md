# Ontelio Censori API Documentation

© 2025 Ontelio, Inc.  
*Document Version:* v1.07.03  
*Last Updated:* 06/21/2025  
*Contact:* support@ontelio.com  

> This document is provided for informational purposes only. Ontelio makes no warranties, express or implied, in this document.

---

## Overview

Ontelio offers APIs for:

- **Transcription**
- **Speaker Diarization**
- **Call Analysis**

### Key Terminology

1. **Transcription** – Extracting spoken content from audio or video into JSON text.
2. **Speaker Diarization** – Segmenting transcription by speaker identity.
3. **Call Analysis** – Evaluating sentiment and emotion at the utterance level, integrating prosody (tone, pitch, pace, and pauses) to understand emotional state and intent.

---

## API Integration Summary

To use Ontelio:

- **Transcription/Diarization:**  
  Endpoint: `{BASE_URL}/transcription`

- **Analytics (Sentiment, Emotion, Prosody, etc.):**  
  Endpoint: `{BASE_URL}/analytics`

### API Call Order

1. **First:** Call the `/transcription` endpoint with the audio file.
2. **Then:** Use the JSON response from transcription as input for any of the following analytics calls:
   - Sentiment
   - Emotion
   - Prosody  
   These can be executed in any order or in parallel.

**Note:** All Ontelio API results are returned via **webhooks**, including a `jobId` for tracking.

---

## Ontelio REST API

### Authentication

- Use the header field `x-api-key` with your assigned API key.

### Base URL



