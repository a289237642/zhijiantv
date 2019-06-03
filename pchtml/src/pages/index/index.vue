<template>
    <div id="index">
        <div class="h1">首页</div>
        <div class="zhijian-container">
            <Table class="zhijian-table" stripe :columns="table.columns" :data="table.data"></Table>
            <div class="zhijian-pagination">
                <Page :total="table.total" :current="table.page" show-elevator @on-change="changePage" :pageSize="table.pagesize"></Page>
            </div>
        </div>
        
    </div>
</template>
<script>
export default {
    name:"index",
    data(){
        return{
            table: {
            page: 1,
            pagesize: 50,
            total: 50,
            columns: [
            {
                title: '账号ID',
                key: 'user_id',
                align: 'center',
                render: (h,params) => {
                let match = false;
                if(this.keyword !== '' && params.row.user_id.toLowerCase().indexOf(this.keyword.toLowerCase()) >= 0) {
                    match = true;
                }else {
                    match = false;
                }
                return h('span',
                    {
                    'class': {
                        match: match
                    }
                    },
                    params.row.user_id
                )
                }
            },
            {
                title: '平台账号',
                key: 'username',
                align: 'center',
                render: (h,params) => {
                let match = false;
                if(this.keyword !== '' && params.row.username.toLowerCase().indexOf(this.keyword.toLowerCase()) >= 0) {
                    match = true;
                }else {
                    match = false;
                }
                return h('span',
                    {
                    'class': {
                        match: match
                    }
                    },
                    params.row.username
                )
                }
            },
            {
                title: '角色',
                key: 'type',
                align: 'center',
            },
            {
                title: '操作员姓名',
                key: 'name',
                align: 'center',
                render: (h,params) => {
                let match = false;
                if(this.keyword !== '' && params.row.name.toLowerCase().indexOf(this.keyword.toLowerCase()) >= 0) {
                    match = true;
                }else {
                    match = false;
                }
                return h('span',
                    {
                    'class': {
                        match: match
                    }
                    },
                    params.row.name
                )
                }
            },
            {
                title: '部门',
                key: 'department',
                align: 'center',
                render: (h,params) => {
                let match = false;
                if(this.keyword !== '' && params.row.department.toLowerCase().indexOf(this.keyword.toLowerCase()) >= 0) {
                    match = true;
                }else {
                    match = false;
                }
                return h('span',
                    {
                    'class': {
                        match: match
                    }
                    },
                    params.row.department
                )
                }
            },
            {
                title: '职位',
                key: 'degree',
                align: 'center',
                render: (h,params) => {
                let match = false;
                if(this.keyword !== '' && params.row.degree.toLowerCase().indexOf(this.keyword.toLowerCase()) >= 0) {
                    match = true;
                }else {
                    match = false;
                }
                return h('span',
                    {
                    'class': {
                        match: match
                    }
                    },
                    params.row.degree
                )
                }
            },
            {
                title: '添加时间',
                key: 'create_time',
                align: 'center',
                width: 110
            },
            {
                title: '操作',
                align: 'center',
                width: 170,
                render: (h, params) => {
                return h(
                    'div',
                    {
                    style: {
                        marginLeft: (params.row.is_admin=='1' || params.row.is_handle=='1')?'0':'-24px'
                    }
                    },
                    [
                    h('i-switch',
                        {
                        attrs: {
                            // title: params.row.status=='0'?'已停用':'已启用'
                        },
                        props: {
                            trueValue: '1',
                            falseValue: '0',
                            value: params.row.status,
                        },
                        style: {
                            display: params.row.is_handle=='1'?'none':'inline-block' //is_handle=='1'表示不能停用启用操作
                        },
                        on: {
                            'on-change': (value) => {
                            this.changeStatus(params.row.user_id,params.row._index, value);
                            }
                        }
                        }
                    ),
                    h('i',
                        {
                        attrs: {
                            class: 'iconfont icon-edit'
                        },
                        style: {

                        },
                        on: {
                            click: () => {
                            this.showEditModal('edit',params.row);
                            }
                        }
                        }
                    ),
                    h('i',
                        {
                        attrs: {
                            class: 'iconfont icon-delete'
                        },
                        style: {
                            display: params.row.is_del=='1'?'none':'inline-block'//is_del=='1'表示不能被删除
                        },
                        on: {
                            click: () => {
                            this.delID = params.row.user_id;
                            this.delModal = true;
                            }
                        }
                        }
                    )
                    ]
                )
                }
            }
            ],
            data: []
        },
        }
    },
    methods: {
        changePage(){

        }
    }
}
</script>
<style lang="scss">
#index{
    height: 100%;
    padding: 20px;
    width: 100%;
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    .h1{
        font-size: 22px;
        color: #808080;
    }
    .zhijian-container{
        margin-top: 20px;
    }
}
</style>
