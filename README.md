# scrap_github


docker-compose up --build
curl http://localhost:6800/schedule.json -d project=scrap_github -d spider=repo_used_by -d repo_name="flask" -d repo_parent=pallets