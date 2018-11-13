#-*- coding:utf8 -*-
from common.httpclient.doRequest import DoRequest

class Solr_Dataimport:
    """
    solr数据导入API说明：
    https://wiki.apache.org/solr/DataImportHandler

    The handler exposes all its API as http requests . The following are the possible operations

    full-import : Full Import operation can be started by hitting the URL http://<host>:<port>/solr/dataimport?command=full-import

        This operation will be started in a new thread and the status attribute in the response should be shown busy now.
        The operation may take some time depending on size of dataset.

        When full-import command is executed, it stores the start time of the operation in a file located at conf/dataimport.properties (this file is configurable)
        This stored timestamp is used when a delta-import operation is executed.
        Queries to Solr are not blocked during full-imports.
        It takes in extra parameters:

            entity : Name of an entity directly under the <document> tag. Use this to execute one or more entities selectively. Multiple 'entity' parameters can be passed on to run multiple entities at once. If nothing is passed, all entities are executed.

            clean : (default 'true'). Tells whether to clean up the index before the indexing is started.

            commit : (default 'true'). Tells whether to commit after the operation.

            optimize : (default 'true' up to Solr 3.6, 'false' afterwards). Tells whether to optimize after the operation. Please note: this can be a very expensive operation and usually does not make sense for delta-imports.

            debug : (default 'false'). Runs in debug mode. It is used by the interactive development mode (see here).
                Please note that in debug mode, documents are never committed automatically. If you want to run debug mode and commit the results too, add 'commit=true' as a request parameter.

    delta-import : For incremental imports and change detection run the command http://<host>:<port>/solr/dataimport?command=delta-import . It supports the same clean, commit, optimize and debug parameters as full-import command.

    status : To know the status of the current command, hit the URL http://<host>:<port>/solr/dataimport . It gives an elaborate statistics on no. of docs created, deleted, queries run, rows fetched, status etc.

    reload-config : If the data-config is changed and you wish to reload the file without restarting Solr. Run the command http://<host>:<port>/solr/dataimport?command=reload-config .

    abort : Abort an ongoing operation by hitting the URL http://<host>:<port>/solr/dataimport?command=abort .
    """
    def __init__(self,url):
        self._url=url
        self._doRequest=DoRequest(self._url)
        self._doRequest.setProxies({'http':'127.0.0.1:8888'})

    def _import(self,coreName,import_type=0,entity=None,clean=False,commit=True,optimize=False,debug=False):
        params={}
        params.update({'entity':entity})
        params.update({'clean':str(clean).lower()})
        params.update({'commit':str(commit).lower()})
        params.update({'optimize':str(optimize).lower()})
        params.update({'debug':str(debug).lower()})
        # post或者get方法都支持
        if 0==import_type:
            httpResponseResult=self._doRequest.post_with_form('/solr/'+coreName+'/dataimport?command=full-import',params=params)
        else:
            httpResponseResult=self._doRequest.post_with_form('/solr/'+coreName+'/dataimport?command=delta-import',params=params)
        return httpResponseResult

    def full_import(self,coreName,entity=None,clean=False,commit=True,optimize=False,debug=False):
        """
        全量导入
        :param coreName:
        :param entity:
        :param clean:
        :param commit:
        :param optimize:
        :param debug:
        :return:
        """
        return self._import(coreName,0,entity,clean,commit,optimize,debug)

    def delta_import(self,coreName,entity=None,clean=False,commit=True,optimize=False,debug=False):
        """
        增量导入
        :param coreName:
        :param entity:
        :param clean:
        :param commit:
        :param optimize:
        :param debug:
        :return:
        """
        return self._import(coreName,1,entity,clean,commit,optimize,debug)