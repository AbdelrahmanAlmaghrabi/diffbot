import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command, LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
import xacro

# This is the function launch system will look for
def generate_launch_description():
    ####### DATA INPUT ##########
    urdf_file_name = 'robot.urdf.xacro'
    package_name = "diff_bot"
    ####### DATA INPUT END ##########
    
    # Launch configuration variables
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    # Declare the launch arguments
    declare_use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation time if true')
    
    print("Fetching URDF ==>")
    # path_to_our_package/urdf/urdf_file
    robot_desc_path = os.path.join(get_package_share_directory(package_name), "urdf", urdf_file_name)
    
    # Process XACRO file
    robot_description_content = xacro.process_file(robot_desc_path).toxml()
    
    # Robot State Publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': robot_description_content
        }]
    )
    
    # Joint State Publisher
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}]
    )
    
    # Create and return launch description object
    return LaunchDescription([
        declare_use_sim_time_arg,
        robot_state_publisher_node,
        joint_state_publisher_node
    ])
