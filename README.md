Веб-приложение распознавания дорожных знаков на изображениях.
# Архитектура
![микросервисная архитектура приложения](https://github.com/Victor90001/deeploma/blob/a55b7561c9ea313d30963b5b81f68820ef0d6880/extra/static/technologies/5.1.png)

- Микросервис API (вы здесь находитесь)
- [Микросервис пользовательского интерфейса](https://github.com/Victor90001/deeploma-webui)
- Микросервис БД

Сервис API будет отвечать за обработку изображений и распознавание дорожных знаков. <br>Принимает изображение и параметры для распознавания, возвращает ответ JSON.<br>

# Docker

[Docker образ API](https://github.com/Victor90001/deeploma/blob/a55b7561c9ea313d30963b5b81f68820ef0d6880/Dockerfile) <br>
[Docker образ WebUI](https://github.com/Victor90001/deeploma-webui/blob/1e4e5dcd6f05c02a2d0973c461bd5aa57387e88e/webui/Dockerfile)

# Kubernetes

Для развертывания использовалась облачная платформа VK Cloud<br>
И их средство управления Kubernetes кластерами.<br>

1. Сервис API <br>
[API Secrets](https://github.com/Victor90001/deeploma/blob/main/extra/Deploy/back/fastapi-secrets.yaml) <br>
[API Deployment+Service](https://github.com/Victor90001/deeploma/blob/a55b7561c9ea313d30963b5b81f68820ef0d6880/extra/Deploy/back/vk_back.yaml)
2. Сервис UI <br>
[UI Deployment+Service](https://github.com/Victor90001/deeploma/blob/a55b7561c9ea313d30963b5b81f68820ef0d6880/extra/Deploy/front/vk-web.yaml)
3. Ingress <br>
[Ingress](https://github.com/Victor90001/deeploma/blob/a55b7561c9ea313d30963b5b81f68820ef0d6880/extra/Deploy/ingress/vk-ingress.yaml) <br>
Ingress Controller:
```bash
helm install ingress-nginx ingress-nginx/ingress-nginx
```

# WebUI
![UI](https://github.com/Victor90001/deeploma/blob/73e01573e663e596b46abacfd65da892971b5b48/extra/static/technologies/web.png)

