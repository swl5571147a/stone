#!/bin/bash
curl -d vender="surface pro" -d product="2014" -d osver="ubuntu 12.04" -d memory=4 -d cpu_model="Intel" -d cpu_num=8 -d sn="xxxx2ss" -d ipaddrs="192.168.1.100:10.1.1.1" -d hostname="bbbbb" http://192.168.1.113:8000/api/collect/
