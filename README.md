# Robot Industri - Rectangle Motion

Simulasi robot differential drive menggunakan ROS 2 Jazzy dan Gazebo Harmonic.

## Deskripsi

Project ini dibuat untuk memenuhi tugas mata kuliah **Robot Industri** di Program Studi Teknik Elektro.

Robot dikendalikan secara otomatis untuk bergerak mengikuti lintasan berbentuk **persegi panjang** pada simulasi Gazebo.

Ukuran lintasan yang digunakan:

* Panjang: 4 meter
* Lebar: 2 meter

Robot menerima perintah kecepatan melalui topic `/cmd_vel` dan menggunakan data odometri dari topic `/odom` untuk menentukan jarak tempuh dan sudut putaran.

## Teknologi

* Ubuntu 24.04
* ROS 2 Jazzy
* Gazebo Harmonic
* Python 3
* `ros_gz_sim`
* `ros_gz_bridge`

## Struktur Project

```text
robot_industri/
├── launch/
│   └── simulation.launch.py
├── package.xml
├── resource/
│   └── robot_industri
├── robot_industri/
│   ├── __init__.py
│   └── rectangle_motion.py
├── setup.cfg
├── setup.py
├── test/
├── urdf/
│   └── robot.urdf.xacro
└── worlds/
    └── robot_world.sdf
```

## Persyaratan

Pastikan sudah terpasang:

* Ubuntu 24.04
* ROS 2 Jazzy
* Gazebo Harmonic
* `ros_gz_sim`
* `ros_gz_bridge`

## Menjalankan Project

### 1. Source ROS 2

```bash
source /opt/ros/jazzy/setup.bash
```

### 2. Masuk ke workspace

```bash
cd ~/robot_industri_ws
```

### 3. Build package

```bash
colcon build --symlink-install
```

### 4. Source workspace

```bash
source ~/robot_industri_ws/install/setup.bash
```

### 5. Jalankan Gazebo

```bash
ros2 launch robot_industri simulation.launch.py
```

Tunggu sampai Gazebo Harmonic terbuka dan robot muncul.

### 6. Jalankan node pergerakan

Buka terminal baru, kemudian jalankan:

```bash
source /opt/ros/jazzy/setup.bash
source ~/robot_industri_ws/install/setup.bash
```

Kemudian:

```bash
ros2 run robot_industri rectangle_motion
```

Robot akan bergerak mengikuti lintasan persegi panjang.

## Topic Utama

### Command Velocity

```text
/cmd_vel
```

Digunakan untuk mengirim perintah kecepatan linear dan angular kepada robot.

### Odometry

```text
/odom
```

Digunakan untuk memperoleh posisi dan orientasi robot selama simulasi.

### TF

```text
/tf
```

Digunakan untuk transformasi koordinat robot.

## Algoritma Pergerakan

Robot melakukan empat sisi lintasan:

```text
        4 meter
    ┌───────────────┐
    │               │
    │               │
 2m │               │
    │               │
    └───────────────┘
        4 meter
```

Urutan gerakan:

1. Maju 4 meter.
2. Berputar 90 derajat.
3. Maju 2 meter.
4. Berputar 90 derajat.
5. Maju 4 meter.
6. Berputar 90 derajat.
7. Maju 2 meter.
8. Berputar 90 derajat.
9. Berhenti.

Program menggunakan data `/odom` untuk memperkirakan jarak yang telah ditempuh dan perubahan orientasi robot.

## Hasil

Robot berhasil bergerak secara otomatis mengikuti lintasan berbentuk persegi panjang pada simulasi Gazebo Harmonic.
