deploy:
	cd /Users/yaroslavyakovenko/Desktop/BOT && \
	git add posts.json && \
	git commit -m "Автоматическое обновление posts.json" && \
	git push heroku main
