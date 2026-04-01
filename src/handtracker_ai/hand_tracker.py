from __future__ import annotations

import time

import cv2
import mediapipe as mp

from .config import AppConfig
from .gesture_engine import GestureEngine
from .models import FrameResult


class HandTracker:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self._mp_hands = mp.solutions.hands
        self._hands = self._mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=config.gesture.detection_confidence,
            min_tracking_confidence=config.gesture.tracking_confidence,
            model_complexity=1,
        )
        self._engine = GestureEngine(config.gesture)
        self._camera = cv2.VideoCapture(config.camera.device_index)
        self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, config.camera.width)
        self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config.camera.height)
        self._camera.set(cv2.CAP_PROP_FPS, config.camera.fps_hint)

    def read(self, track_enabled: bool = True) -> FrameResult | None:
        started_at = time.perf_counter()
        ok, frame = self._camera.read()
        if not ok:
            return None

        frame = cv2.flip(frame, 1)
        if not track_enabled:
            self._engine.classify(None)
            latency_ms = (time.perf_counter() - started_at) * 1000
            return FrameResult(
                frame_bgr=frame,
                prediction=None,
                latency_ms=latency_ms,
                hand_landmarks=None,
            )

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self._hands.process(rgb_frame)

        prediction = None
        hand_landmarks = None
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            self._draw_landmarks(frame, hand_landmarks)
            prediction = self._engine.classify(hand_landmarks)
        else:
            self._engine.classify(None)

        latency_ms = (time.perf_counter() - started_at) * 1000
        return FrameResult(
            frame_bgr=frame,
            prediction=prediction,
            latency_ms=latency_ms,
            hand_landmarks=hand_landmarks,
        )

    def pointer_target(self, frame_result: FrameResult):
        if frame_result.hand_landmarks is None:
            return None
        return self._engine.pointer_target(frame_result.hand_landmarks)

    def _draw_landmarks(self, frame, hand_landmarks) -> None:
        frame_height, frame_width = frame.shape[:2]

        for connection in self._mp_hands.HAND_CONNECTIONS:
            start = hand_landmarks.landmark[connection[0]]
            end = hand_landmarks.landmark[connection[1]]
            start_point = (int(start.x * frame_width), int(start.y * frame_height))
            end_point = (int(end.x * frame_width), int(end.y * frame_height))
            cv2.line(frame, start_point, end_point, (255, 255, 255), 2, cv2.LINE_AA)

        for landmark in hand_landmarks.landmark:
            point = (int(landmark.x * frame_width), int(landmark.y * frame_height))
            cv2.circle(frame, point, 4, (255, 255, 255), -1, cv2.LINE_AA)
            cv2.circle(frame, point, 7, (30, 30, 30), 1, cv2.LINE_AA)

    def close(self) -> None:
        self._camera.release()
        self._hands.close()
