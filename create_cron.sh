#!/bin/bash

#每日抓取更新数据
echo '#!/bin/bash' > img_daily.sh
echo 'cd '$(pwd) >> img_daily.sh
echo 'scrapy crawl bcy_daily' >>img_daily.sh

#将抓取作为每日任务
echo '0 11 * * * '$(pwd)'/img_daily.sh' > cron.temp
crontab cron.temp
rm -rf cron.temp

#后续更新时避免覆盖配置文件
git update-index --skip-worktree  scrapy_test/db.py
git update-index --skip-worktree  scrapy_test/settings.py
