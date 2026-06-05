---
title: Hello World
date: 2026-06-05
tags: [hello, unix, c-language, blog]
description: 第一篇博客文章，介绍自己和兴趣爱好
---

# Hello
你好！这是我的第一篇贴子。我是Leo，来自福建厦门的一个学生。

```sh
$ echo "我喜欢研究UNIX的历史，并且创作了相关的小说。" > hello.txt
$ echo "同时我还会一点C语言。" >> hello.txt
$ ls
hello.txt hello.c
$ cc hello.c -o hello
$ ./hello
执行命令：cat hello.txt
我喜欢研究UNIX的历史，并且创作了相关的小说。
同时我还会一点C语言。
$ 
```
