import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():

    package_dir = get_package_share_directory('robot_industri')

    urdf_file = os.path.join(
        package_dir,
        'urdf',
        'robot.urdf.xacro'
    )

    world_file = os.path.join(
        package_dir,
        'worlds',
        'robot_world.sdf'
    )

    # Gazebo Harmonic
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args': f'-r {world_file}'
        }.items()
    )

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[
            {
                'robot_description': open(urdf_file).read()
            }
        ]
    )

    # Spawn robot ke Gazebo
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
    '-world', 'robot_world',
    '-file', urdf_file,
    '-name', 'industrial_robot',
    '-x', '0',
    '-y', '0',
    '-z', '0.5',
    '-R', '0',
    '-P', '0',
    '-Y', '0'
],
        output='screen'
    )
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
        ],
        output='screen'
    )
    return LaunchDescription([
    gazebo,
    robot_state_publisher,
    spawn_robot,
    bridge,
])
