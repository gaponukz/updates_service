# Server update / client download... service
## Installation
Clone this git repo
```bash
git clone https://github.com/gaponukz/updates_service.git
```
Go to the root directory
```bash
cd updates_service
```
## Setuping
Install all dependencies
```bash
pip install -r requirements.txt
```
Setuping some configuration in env:
```env
ADMIN_PASSWORD_KEY=12345
```
## Starting
With unicorn
```bash
uvicorn main:app --log-config log.ini
```
