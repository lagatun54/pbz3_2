# ПБЗ 3 лаба (2-ой семестр) 

Команда если кто-то захочет запустить с mac на arm 

```bash
docker run --platform "linux/amd64" -d -e AGRAPH_SUPER_USER=test -e AGRAPH_SUPER_PASSWORD=xyzzy -p 10000-10035:10000-10035 --shm-size 1g --name agraph --restart=always franzinc/agraph
```

А там дальше подгружаем либы с requirements.txt
```bash
pip install -r requirements.txt
```
и запускаем проект 

```bash
python3 main.py
```

