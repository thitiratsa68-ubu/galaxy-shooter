# Galaxy Shooter

เกมยิงอวกาศแนวอาร์เคด 2D ที่สร้างด้วย Pygame เน้นเล่นสั้น ๆ ยิงศัตรู เก็บคะแนน และเปลี่ยนบรรยากาศเมื่อเก่งขึ้น

## Project Description
ผู้เล่นบังคับยานซ้าย–ขวา แล้วยิงศัตรูที่ตกลงมา หลีกกระสุนเก็บชีวิตจนกว่าจะได้คะแนนสูงสุด เปลี่ยนฉากและศัตรูชุดใหม่อัตโนมัติเมื่อคะแนนถึงเกณฑ์

## Team Members
- เพิ่มชื่อสมาชิก/บทบาทที่นี่ (เช่น ผู้พัฒนา, ผู้ออกแบบเสียง)

## Technologies Used
- Python 3.12
- Pygame 2.6.x (`requirements.txt`)
- Standard Library (`pathlib`, `math`, `random`)

## OOP Concepts Used
- การสืบทอดคลาส: `Player`, `Enemy`, `Bullet` สืบทอดจาก `pygame.sprite.Sprite`
- การห่อหุ้ม (encapsulation): เมธอด `_load_*` จัดการโหลดทรัพยากรภายในคลาส
- การประกอบวัตถุ (composition): `GameScene` จัดกลุ่ม `sprites`/`enemies`/`bullets` และถือออบเจกต์ `Player`
- การใช้ class variable เพื่อแคชทรัพยากร (flyweight-style) ใน `Player` และ `Enemy`

## Design Patterns Used
- Scene/State pattern อย่างง่าย: สลับ `StartMenu` → `GameScene` ภายใน `main.py`
- Factory-ish method: `_create_enemy()` ปรับภาพและความเร็วศัตรูตามคะแนน
- Asset loader helper: `utils/assets.py` เลือกไฟล์ภาพแรกที่มีอยู่ ลดโค้ดซ้ำ

## Project Structure
```
.
├─ main.py               # จุดเริ่มโปรแกรม สลับฉากเมนู/เกม
├─ config.py             # ค่าคงที่ของเกม (จอ, ความเร็ว, ทรัพยากร)
├─ scenes/
│  ├─ start_menu.py      # หน้าจอเริ่มเกม + แถบโหลด
│  └─ game_scene.py      # ลูปเกมหลัก ระบบคะแนน/ชีวิต
├─ sprites/
│  ├─ player.py          # การเคลื่อนที่และยิงกระสุน
│  ├─ enemy.py           # ศัตรูตกจากด้านบน ปรับความเร็วตามคะแนน
│  └─ bullet.py          # กระสุนและอายุการใช้งาน
├─ utils/assets.py       # ฟังก์ชันช่วยโหลดภาพแรกที่พบ
├─ assets/               # รูปและเสียงสำรองหลายชื่อไฟล์
├─ requirements.txt
└─ pyproject.toml
```

## Installation
- ติดตั้ง Python 3.12
- แนะนำสร้าง virtualenv: `python -m venv .venv && source .venv/bin/activate` (หรือ `Scripts\activate` บน Windows)
- ติดตั้งไลบรารี: `pip install -r requirements.txt`

## How to Run
- เปิด virtualenv (ถ้ามี) แล้วรัน `python main.py`
- ปิดเกมด้วยการกดปุ่มปิดหน้าต่างหรือ `ESC`

## Features
- เมนูเริ่มพร้อมแถบโหลด กด Space/Enter/คลิกเพื่อข้าม
- ปุ่ม Start/Restart ในฉากเกม ใช้งานได้ทั้งเมาส์และคีย์บอร์ด (R)
- ยิงกระสุนได้ทันทีด้วย Space พร้อมเสียงยิงสังเคราะห์ถ้าไม่มีไฟล์เสียงจริง
- ศัตรูสุ่มตำแหน่ง/ความเร็ว เพิ่มความยากตามคะแนน และเปลี่ยนชุดภาพเมื่อได้ ≥100 คะแนน
- ระบบคะแนนและชีวิตแบบหัวใจ 3 ดวง พร้อม HUD มุมซ้ายบน
- เปลี่ยนฉากหลังอัตโนมัติถ้ามีไฟล์พื้นหลังด่าน 2 ใน `assets/`

## Demo
- มีภาพตัวอย่างการเล่นในโฟลเดอร์ `sceen.png/` (สามารถแทรกเป็น Markdown image ได้)
- ต้องการ GIF/วีดีโอ: บันทึกหน้าจอขณะรัน `python main.py` แล้ววางไฟล์ไว้ใน `assets/` หรืออัปโหลดตามต้องการ
