# media_work_model

my self working model everyday

### install

#pip list --format=freeze > requirements.txt
#distribute，pip，setuptools，wheel 需要删除

git clone git@github.com:aceliuchanghong/media_work_model.git

conda create -n worker python=3.10

conda activate worker

pip install -r requirements.txt --proxy=127.0.0.1:10809
