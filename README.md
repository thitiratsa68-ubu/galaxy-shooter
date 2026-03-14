# Galaxy Shooter (สาธิต OOP + SOLID)

## ทีม
- ชื่อทีม: Galaxy Learners
- สมาชิก: เพิ่มรายชื่อและรหัสนักศึกษาที่นี่

## การติดตั้งและรัน
1. ใช้ Python 3.12 ขึ้นไป
2. ติดตั้งไลบรารี (เลือกหนึ่งวิธี)
   - `pip install -r requirements.txt`
   - หรือ `pip install .` (อ่านจาก `pyproject.toml`)
3. รันเกมด้วยคำสั่ง `python main.py`

## ตัวอย่างการใช้ OOP ในโค้ด
- Inheritance (การสืบทอด): `Player`, `StraightEnemy`, `ZigZagEnemy`, `Bullet` สืบทอดจาก `SpaceObject` (`sprites/base.py`).
- Polymorphism (พหุรูป): ศัตรูแต่ละชนิด override เมธอด `update()` เคลื่อนที่ต่างรูปแบบ และ `EnemyFactory` จ่ายศัตรูชนิดใดก็ได้ผ่านอินเทอร์เฟซเดียวกัน
- Encapsulation (การห่อหุ้ม): `ScoreBoard` เก็บและวาดคะแนน/พลังชีวิต, `Weapon` จัดการคูลดาวน์การยิง พร้อมพร็อพเพอร์ตีควบคุมค่าภายใน
- Composition (องค์ประกอบ): `GameScene` รวม `Player`, `EnemyFactory`, `ScoreBoard`; ภายใน `Player` ประกอบ `Weapon` เพื่อสร้างกระสุน

## การแมปกับหลักการ SOLID
- Single Responsibility: `ScoreBoard` มีหน้าที่วาด HUD, `Weapon` ดูแลการยิง, `EnemyFactory` สร้างศัตรู
- Open/Closed: เพิ่มคลาสศัตรูใหม่แล้วลงทะเบียนใน `EnemyFactory` ได้โดยไม่แก้ลอจิกเกม
- Liskov Substitution: ออบเจ็กต์ที่สืบทอด `SpaceObject` ใด ๆ ใช้ใน sprite group ได้เหมือนกัน; ศัตรูที่สืบทอด `BaseEnemy` แทนกันได้
- Interface Segregation: แยกคลาสขนาดเล็กตามหน้าที่ (`Weapon`, `ScoreBoard`) เลี่ยงอินเทอร์เฟซกว้างเกินไป
- Dependency Inversion: `GameScene` พึ่งพา abstraction `EnemyFactory` แทนการผูกกับคลาสศัตรูจริง; `Player` พึ่ง `Weapon` สำหรับการยิง

## โครงสร้างโฟลเดอร์
- `main.py` — เปิดหน้าต่าง pygame และส่งต่อให้ `GameScene`
- `scenes/game_scene.py` — ควบคุมลูปเกมและตรวจชน
- `sprites/base.py` — คลาสฐานของสไปรต์ทั้งหมด
- `sprites/player.py` — การควบคุมผู้เล่นและการประกอบอาวุธ
- `sprites/weapon.py` — การสร้างกระสุนและจัดการคูลดาวน์
- `sprites/enemy.py` — คลาสฐานศัตรูและพฤติกรรมศัตรูผ่านแฟกทอรี
- `sprites/bullet.py` — พฤติกรรมกระสุน
- `assets/` — ไฟล์ภาพพื้นหลัง ผู้เล่น ศัตรู

## การบังคับ
- เคลื่อนที่: ปุ่มลูกศร
- ยิง: Space bar
- เริ่มใหม่เมื่อ Game Over: กด `R`

## หมายเหตุสำหรับผู้ตรวจ
- ได้คะแนน 10 ต่อศัตรูที่ถูกทำลาย ระดับความยากเพิ่มตามคะแนน
- ศัตรูสองแบบ (วิ่งตรงและซิกแซก) แสดงตัวอย่างพหุรูปในรันไทม์
