# Mouse walking maze [[OpenAI Gym](https://gym.openai.com/)] (開發中)
<img src="./img/default_map.gif" align="right"/>

[![Build Status](https://dev.azure.com/KennethTang/github/_apis/build/status/NTUT-SELab.mouse-walking-maze.gym?branchName=master)](https://dev.azure.com/KennethTang/github/_build/latest?definitionId=3&branchName=master)
![Azure DevOps coverage](https://img.shields.io/azure-devops/coverage/KennethTang/github/3)

這是一個簡單的老鼠走迷宮 [OpenAI Gym](https://gym.openai.com/) 環境，這個環境包含了 3 種子環境:

1. 發生無效動作時，不進行任何的獎勵給予或動作屏蔽
1. 發生無效動作時，給予一個負獎勵
1. 發生無效動作時，使用動作遮罩屏蔽代理人的動作選擇

目的是為了驗證代理人受到環境的限制而出現大量的無效動作時，採用上述 ３ 種方法其效果如何。
