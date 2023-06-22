# Server update / client download... service
Before start:
 + Setup some configuration in env:
```env
ADMIN_PASSWORD_KEY=12345
```
 + Create `database` folder with that files:
```
root
│   versions.json
│   
└───versions
        build1.zip
        build2.zip
        ...
        buildn.zip
```
Where `versions.json` is empty list:
```json
[]
```
## Deploying locally
Clone this git repo
```bash
git clone https://github.com/gaponukz/updates_service.git
```
Install all dependencies
```bash
pip install -r requirements.txt
```
Starting with unicorn
```bash
uvicorn main:app --log-config log.ini
```
## Deploying from Docker ~~hub~~
Build in image
```bash
docker build -t updates-service .
```
Starting container
```bash
docker run -d -p 8000:8000 --rm --env-file .env -v "path/to/database:/app/database"  updates-service
```
