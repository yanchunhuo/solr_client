# [solr客户端]()
# [概况]()
* 对solr进行操作

# [使用]()
## 一、环境准备
### 1、安装python依赖模块
* pip install -r requirements.txt

### 2、操作数据导入
```python
from solr.solr_dataimport import Solr_Dataimport
if __name__=='__main__':
    solr_dataimport=Solr_Dataimport('http://127.0.0.1:8881')
    solr_dataimport.delta_import('coreName','coreEntity')
```

# [打赏]()
![avatar](https://github.com/yanchunhuo/resources/blob/master/Alipay.jpg)


