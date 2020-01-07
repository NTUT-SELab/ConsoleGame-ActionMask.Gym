# Mouse walking maze [[OpenAI Gym](https://gym.openai.com/)]
<img src="./img/default_map.gif" align="right"/>

[![Build Status](https://dev.azure.com/KennethTang/github/_apis/build/status/NTUT-SELab.ConsoleGame-ActionMask.Gym?branchName=master)](https://dev.azure.com/KennethTang/github/_build/latest?definitionId=4&branchName=master)
[![Azure DevOps coverage](https://img.shields.io/azure-devops/coverage/KennethTang/github/4)](https://dev.azure.com/KennethTang/github/_build/latest?definitionId=4&branchName=master)

這是一個簡單的老鼠走迷宮 [OpenAI Gym](https://gym.openai.com/) 環境，這個環境包含了 3 種子環境:

1. 發生無效動作時，不進行任何的獎勵給予或動作屏蔽 ([BaseEnv](./env/MouseWalkingMaze/base_env.py))
1. 發生無效動作時，給予一個負獎勵 ([NegativeRewardEnv](./env/MouseWalkingMaze/negative_reward_env.py))
1. 發生無效動作時，使用動作遮罩屏蔽代理人的動作選擇 ([ActionMaskEnv](./env/MouseWalkingMaze/action_mask_env.py))

目的是為了驗證代理人受到環境的限制而出現大量的無效動作時，採用上述 ３ 種方法其效果如何。

## [地圖資訊定義](./env/map_define.py)
```
道路 = ' '
牆壁 = 'X'
出口 = 'E'
老鼠 = 'M'
食物 = 'F'
毒藥 = 'P'
```

## 如何使用

**1.** Clone `stable-baselines` 支援 `Action maske` 的版本
```
git clone https://github.com/NTUT-SELab/stable-baselines
cd stable-baselines
git checkout neglogp+entropy
cd ..
```
**2.** Clone 這個 Repositorie
```
git clone https://github.com/NTUT-SELab/mouse-walking-maze.gym
cd mouse-walking-maze.gym
```

**3.** 執行範例
- 使用 Docker

> SB_PATH是 `stable-baselines` 專案存放的路徑
> ```
> SB_PATH=/homes/user/stable-baselines/ ./scripts/run_docker_gpu.sh python ./examples/MouseWalkingMaze/default_map/run_base_env.py
> ```
> 使用GPU請參考: [Build and run Docker containers leveraging NVIDIA GPUs](https://github.com/NVIDIA/nvidia-docker)

- 直接執行
> ```
> python3 ./examples/MouseWalkingMaze/default_map/run_base_env.py
> ```
