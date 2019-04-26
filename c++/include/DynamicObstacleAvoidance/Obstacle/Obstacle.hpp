/**
 * @class Obstacle
 * @brief Class to define the obstacles
 * @author Baptiste Busch
 * @date 2019/04/16
 */

#ifndef DYNAMIC_OBSTACLE_AVOIDANCE_OBSTACLE_OBSTACLE_H_
#define DYNAMIC_OBSTACLE_AVOIDANCE_OBSTACLE_OBSTACLE_H_

#include <eigen3/Eigen/Core>
#include "DynamicObstacleAvoidance/State/State.hpp"
#include "DynamicObstacleAvoidance/State/Pose.hpp"
#include <iostream>

class Obstacle 
{
private:
	State state;
	Eigen::Vector3f reference_position;

	float safety_margin;

public:
	explicit Obstacle(const State& state, const float& safety_margin=0);
	explicit Obstacle(const State& state, const Eigen::Vector3f& reference_position, const float& safety_margin=0);
	~Obstacle();

	inline const State get_state() const 
	{ 
		return this->state;
	}

	inline const Pose get_pose() const 
	{ 
		return this->state.get_pose();
	}

	inline const Eigen::Vector3f get_position() const 
	{ 
		return this->state.get_position();
	}

	inline const Eigen::Quaternionf get_orientation() const 
	{ 
		return this->state.get_orientation();
	}

	inline const Eigen::Vector3f get_linear_velocity() const
	{
		return this->state.get_linear_velocity();
	}

	inline const Eigen::Vector3f get_angular_velocity() const
	{
		return this->state.get_angular_velocity();
	}

	inline const Eigen::Vector3f get_reference_position() const
	{
		return this->reference_position;
	}

	inline float get_safety_margin() const
	{ 
		return this->safety_margin;
	}

	inline void set_pose(const Pose& pose)
	{
		this->state.set_pose(pose);
	}

	inline void set_position(const Eigen::Vector3f& position)
	{
		this->state.set_position(position);
	}

	inline void set_orientation(const Eigen::Quaternionf& orientation)
	{
		this->state.set_orientation(orientation);
	}

	inline void set_linear_velocity(const Eigen::Vector3f& linear_velocity)
	{
		this->state.set_linear_velocity(linear_velocity);
	}

	inline void set_angular_velocity(const Eigen::Vector3f& angular_velocity)
	{
		this->state.set_angular_velocity(angular_velocity);
	}

	virtual Eigen::Vector3f compute_normal_to_external_point(const Eigen::Vector3f& external_point) const;
	
	virtual float compute_distance_to_external_point(const Eigen::Vector3f& external_point) const;
};

#endif