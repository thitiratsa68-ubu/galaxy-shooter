import io
import math
import random
import wave
from pathlib import Path
import pygame


class SoundManager:
    """ดูแลโหลด/เล่นเสียง พร้อม fallback สร้างเสียงสังเคราะห์ถ้าไม่มีไฟล์ใน assets."""

    def __init__(self):
        self._ensure_mixer()
        self._last_play = {"shoot": 0, "explosion": 0, "hit": 0}
        self._play_gap_ms = 80  # กันเล่นซ้อนถี่เกิน ลดโอกาสแตก
        self.shoot_sound = self._load_sound([
            Path("assets/sfx_shoot.wav"),
            Path("assets/sfx_shoot.ogg"),
        ], self._generate_shoot_tone)

        self.explosion_sound = self._load_sound([
            Path("assets/sfx_explosion.wav"),
            Path("assets/sfx_explosion.ogg"),
        ], self._generate_explosion_noise)

        self.hit_sound = self._load_sound([
            Path("assets/sfx_hit.wav"),
            Path("assets/sfx_hit.ogg"),
        ], self._generate_hit_thump)

        # ปรับระดับเสียงรวมให้ไม่ peak
        for s in (self.shoot_sound, self.explosion_sound, self.hit_sound):
            if s:
                s.set_volume(0.5)

    def _ensure_mixer(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
        pygame.mixer.set_num_channels(12)

    def _load_sound(self, candidates, fallback_factory):
        for path in candidates:
            if path.exists():
                try:
                    return pygame.mixer.Sound(str(path))
                except pygame.error:
                    continue
        return pygame.mixer.Sound(file=io.BytesIO(fallback_factory()))

    def _generate_shoot_tone(self, freq=660, duration=0.08, volume=0.35):
        """โทนยิงแบบนุ่ม ใช้ sine + tone ปิดท้าย octave ขึ้นเล็กน้อย"""
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        buf = bytearray()
        for i in range(n_samples):
            t = i / sample_rate
            # envelope แบบ fade-out เร็วเพื่อลดความแหลม
            env = max(0.0, 1.0 - t / duration)
            base = math.sin(2 * math.pi * freq * t)
            overtone = 0.3 * math.sin(2 * math.pi * freq * 1.5 * t)
            sample = int(volume * env * 28000 * (base + overtone))
            buf += sample.to_bytes(2, byteorder="little", signed=True)
        return self._wrap_wav(buf, sample_rate)

    def _generate_explosion_noise(self, duration=0.28, volume=0.32):
        """เสียงระเบิดแบบนุ่ม ใช้ noise + decay ช้า"""
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        buf = bytearray()
        for i in range(n_samples):
            t = i / sample_rate
            env = math.exp(-4 * t)  # decay เร็วช่วงแรกแล้วนุ่มลง
            sample = int((random.random() * 2 - 1) * 30000 * volume * env)
            buf += sample.to_bytes(2, byteorder="little", signed=True)
        return self._wrap_wav(buf, sample_rate)

    def _generate_hit_thump(self, freq=220, duration=0.18, volume=0.35):
        """เสียงชนทุ้มสั้น ๆ ไม่ตกใจ ใช้ sine + decay ช้าเล็กน้อย"""
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        buf = bytearray()
        for i in range(n_samples):
            t = i / sample_rate
            env = math.exp(-6 * t)
            sample = int(volume * env * 28000 * math.sin(2 * math.pi * freq * t))
            buf += sample.to_bytes(2, byteorder="little", signed=True)
        return self._wrap_wav(buf, sample_rate)

    def _wrap_wav(self, pcm_bytes: bytearray, sample_rate: int):
        bio = io.BytesIO()
        with wave.open(bio, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(pcm_bytes)
        bio.seek(0)
        return bio.read()

    def play_shoot(self):
        now = pygame.time.get_ticks()
        if self.shoot_sound and now - self._last_play["shoot"] > self._play_gap_ms:
            self.shoot_sound.play()
            self._last_play["shoot"] = now

    def play_explosion(self):
        now = pygame.time.get_ticks()
        if self.explosion_sound and now - self._last_play["explosion"] > self._play_gap_ms:
            self.explosion_sound.play()
            self._last_play["explosion"] = now

    def play_hit(self):
        now = pygame.time.get_ticks()
        if self.hit_sound and now - self._last_play["hit"] > self._play_gap_ms:
            self.hit_sound.play()
            self._last_play["hit"] = now
