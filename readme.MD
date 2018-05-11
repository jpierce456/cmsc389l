# Pomodoro Dash Button

CMSC389L Final Project

## Overview

The Pomodoro dash button allows a user to use an [Amazon Dash Button](https://aws.amazon.com/iotbutton/) to easily adhere to the Pomodoro Study technique.  The Pomodoro study technique follows cycles of 25 minutes of work followed by 5 minutes of rest, with a longer 10-15 minute break after 3-4 cycles.  The user simply pushes the dash button with a single, double, or long click in order to do a 25 minute work session, short break, or long break respectively.  The user will recieve a text message after the period of time is up, notifying them to proceed to the next stage.

## Services Used

- IoT
- DynamoDB
- SNS
- Lambda

## Architecture

![Click here to view the architecture diagram](https://cloudcraft.co/view/9a40b885-d871-49c6-a4bd-f33ced8823c1?key=04oM17g6aihON4JfXvibUw)

## Video Demo

![Click here to view the youtube demo](https://www.youtube.com/watch?v=PGfqijcSeLw)

## Recreation Notes

 - Must have an AWS IoT button purchased and configured
 - Create an IAM Role with the policy in policy.json
 - Create an SNS topic with the endpoint of the phone number you want to send notifications to.