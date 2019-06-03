<template>
    <div id="ActivityList">
       <div class="h1">活动列表</div>
        <!-- 新增 -->
        <div class="header">
            <Button class="newbtn zhijian-new-btn" type="primary" @click="showEditModal('new')">新增</Button>
        </div>
        <Table class="zhijian-table account-table" stripe :columns="table.columns" :data="table.data"></Table>
        <div class="zhijian-pagination">
            <Page :total="table.total" :current="table.page" show-elevator @on-change="changePage" :pageSize="table.pagesize"></Page>
        </div>
        <!-- 新增、编辑弹框 -->
        <Modal :mask-closable="false" v-model="editModal" width="535" class-name="ma-edit-modal">
            <div class="edit-modal-body">
                <Icon type="android-close" @click="editModal=false"></Icon>
                <div v-if="formValidate.type=='new'" class="title">新增活动</div>
                <div v-if="formValidate.type=='edit'" class="title">编辑活动信息</div>
                <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80">
                    <FormItem label="排序" prop="sort">
                        <Input v-model="formValidate.sort" placeholder="请输入排序号"></Input>
                    </FormItem>
                    <FormItem label="活动标题" prop="title">
                        <Input v-model="formValidate.title" placeholder="请输入活动标题"></Input>
                    </FormItem>
                    <FormItem label="上传图片" prop="uploadimg">
                        <div class="h5ImgBox" v-if="isShow">
                            <img :src="h5Img" style="width:98px;height:98px;">
                        </div>
                        <div >
                            <label for="inputFile" class="button">
                            <span class="upload__select">点击上传图片</span>
                            <input type="file" id="inputFile" accept="image/gif, image/jpeg, image/png, image/jpg" style="display:none" @change="onUpload">
                            </label>
                        </div>
                    </FormItem>
                    <FormItem label="跳转链接" prop="link">
                        <Input v-model="formValidate.link" placeholder="请输入链接"></Input>
                    </FormItem>
                    <FormItem label="标签">
                        <Input v-model="formValidate.tag" placeholder="请输入标签"></Input>
                    </FormItem>
                    <FormItem label="状态" prop="status">
                        <RadioGroup v-model="formValidate.status">
                            <Radio label="1">启用</Radio>
                            <Radio label="0">禁用</Radio>
                        </RadioGroup>
                    </FormItem>
                </Form>
            </div>
            <div class="zhijian-btn-box">
                <div class="zhijian-btn-confirm" @click="submitForm('formValidate')">确定</div>
            </div>
        </Modal>
    </div>
</template>
<script>
export default {
    name:"ActivityList",
    data(){
        const validateImg = (rule, value, callback) => {
            if (this.h5Img == '') {
                callback(new Error("请上传图片(大小不超过2M, 只支持png,jpg,jpeg,gif,bmp格式)"));
            } else {
                callback();
            }
        };
        return{
            table: {
                page: 1,
                pagesize: 10,
                total: 50,
                columns: [
                    {
                        title: '活动id',
                        key: 'activityid',
                        width: 100,
                        align: 'center'
                    },
                    {
                        title: '排序',
                        key: 'sort',
                        // width:100,
                        align: 'center'
                    },
                    {
                        title: '活动标题',
                        key: 'title',
                        // width:300,
                        align: 'center'
                        
                    },
                    {
                        title: '活动图片',
                        key: 'main_img',
                        // width:100,
                        align: 'center',
                        render: (h,params)=>{
                          return h ('img',{
                            attrs: {
                              src: params.row.main_img
                            },
                            style: {
                              width: '35px',
                              height: '35px',
                            }
                          })
                        }
                    },
                    {
                        title: '跳转链接',
                        key: 'link',
                        // width:400,
                        align: 'center'
                    },
                    {
                        title: '标签',
                        // width:150,
                        key: 'tag',
                        align: 'center'
                    },
                    {
                        title: '操作',
                        align: 'center',
                        // width: 400,
                        render: (h, params) => {
                        return h('div',[
                                h('i',{
                                        attrs: {
                                            class: 'iconfont icon-edit'
                                        },
                                        on: {
                                            click: () => {
                                                this.showEditModal('edit',params.row);
                                            }
                                        }
                                    }
                                ),
                                h('i-switch',{
                                        attrs: {
                                            title: params.row.status=="0"?'已停用':'已启用'
                                        },
                                        props: {
                                            value: params.row.status,
                                            trueValue: "1",
                                            falseValue: "0"
                                            
                                        },
                                        on: {
                                            'on-change': (value) => {
                                                this.changeStatus(params.row.id,params.row._index, value);
                                            }
                                        }
                                    }
                                ),
                            ]
                        )
                        }
                    }
                ],
                data: []
            },
            isShow:false,// 显示图片
            editModal: false, // 新增编辑弹框
            h5Img:'',
            formValidate: {
                type: 'new',
                row: {},
                title:'',
                sort:'',
                tag:'',
                main_img:'',
                link:'',
                status:'1'
            },
            ruleValidate:{
                sort:[
                    { required: true, message: '请输入排序号',pattern:/^[0-9]*$/, trigger: 'blur' }
                ],
                title: [
                    { required: true, message: '请输入标题', trigger: 'blur' }
                ],
                uploadimg:[
                    { 
                        required: true,
                        validator: validateImg, 
                        trigger: "blur" ,
                    }
                ],
                link: [
                    { required: true, message: '请输入链接', trigger: 'blur' }
                ],
                status: [
                    { required: true, message: '请选择状态', trigger: 'change' }
                ]
            }
        }
    },
    created() {
        this.getData();
    },
    methods: {
        getData() {
            this.$http.post(this.PATH.GETPCACTIVITY,{
                page: this.table.page,
                size:this.table.pagesize
            }).then(res=>{
                // console.log(res.data)
                if (res.data.status == 0) {
                    this.table.data = res.data.list
                    this.table.total = res.data.total
                } else {
                    this.$Modal.error({
                        width: 360,
                        content: res.data.errmsg
                    })
                }
            })
        },
        //分页
        changePage(page) {
            this.table.page = page
            this.getData()
        },
        // 开启、停用活动
        changeStatus(id, index, nValue) {
            // console.log('id:',id, ' index:',index, ' nValue:',nValue,' this.table.data[index].status:',this.table.data[index].status)
            let msg = '该活动已开启';
            if(nValue == '0') {
                msg = '该活动已停止使用';
            }
            this.$http
                .post(this.PATH.CHANGESTATUS, {
                    id: id,
                    status:this.table.data[index].status
                })
                .then(res => {
                if(res.data.status == '0') {
                    // console.log(res.data)
                    this.table.data[index].status=nValue;
                }else {
                    //如果发请求失败，状态回滚：
                    this.table.data[index].status = nValue=='1'?'0':'1';
                    this.$Modal.error({
                        width: 360,
                        content: res.data.msg
                    })
                }
                this.getData();
            })
        },
        //展示弹框
        showEditModal(type, row) {
            // console.log(name)
            // 显示新增活动、编辑
            this.editErrorTip = false;
            this.formValidate.type = type;
            //对整个表单进行重置，将所有字段值重置为空并移除校验结果
            this.$refs.formValidate.resetFields();
            if(type == 'new') {
                this.formValidate.id = '';
                this.isShow = false;
                this.formValidate.tag='';
                this.h5Img='';
                this.formValidate.row = {
                    id: '',
                    title: '',
                    sort: '',
                    link: ' ',
                    status: '1',
                    tag: ''
                };
            }else{
                // console.log(row)
                this.isShow = true;
                this.h5Img = row.main_img;
                this.formValidate.id = row.id;
                this.formValidate.title = row.title;
                this.formValidate.sort = row.sort;
                this.formValidate.link = row.link;
                this.formValidate.status = row.status;
                this.formValidate.tag = row.tag;
            }
            this.editModal = true;
        },
        submitForm(name){
            this.$refs[name].validate((valid) => {
                if (valid) {
                    let type = this.formValidate.type;
                    let path = '';
                    let params = new Object();
                    if(type == 'new') {
                        //新增
                        path = this.PATH.CREATEACTIVITY;
                        params = {
                            title:this.formValidate.title,
                            sort:this.formValidate.sort,
                            link:this.formValidate.link ,
                            status:this.formValidate.status,
                            tag:this.formValidate.tag,
                            main_img:this.h5Img
                        }
                    }else{
                        path = this.PATH.CHANGEACTIVITY;
                        params = {
                            id: this.formValidate.id,
                            title:this.formValidate.title,
                            sort:this.formValidate.sort,
                            link:this.formValidate.link ,
                            status:this.formValidate.status,
                            tag:this.formValidate.tag,
                            main_img:this.h5Img
                        }
                    }
                    this.$http.post(path,params).then(
                        success =>{
                            // console.log(success.data)
                           if(this.formValidate.type == 'new') {
                               this.$Modal.success({
                                    title:'提示',
                                    content: success.data.msg,
                                    onOk: () => {
                                        this.editModal = false;
                                    },
                                });
                           }else{
                               this.$Modal.success({
                                    title:'提示',
                                    content: success.data.msg,
                                    onOk: () => {
                                        this.editModal = false;
                                    },
                                });
                           }
                           this.table.page = 1;
                           this.getData(); 
                        }
                    )
                } else {
                    this.$Message.error('Fail!');
                }
            })
        },
        //上传图片
        onUpload(e){
            let files = e.target.files || e.dataTransfer.files;
            if (!files.length) return;
            let type = e.target.files[0].type;
            let typeArr = ['png','jpg','jpeg','gif','bmp'];
            // if(type == "" || typeArr.indexOf(type.split("/")[1])<0 || e.target.files[0].size >2*1024*1024) {
            //     this.h5Img = '';
            //     this.$refs.formValidate.validateField("qrcard")
            //     return;
            // }
            var reads= new FileReader();
            reads.readAsDataURL(files[0]);
            let that = this;
            // console.log(reads)
            reads.onload=function (e) {
                var fd = new FormData()
                fd.append('data', this.result)
                let config = {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
                // console.log(this.result)
                that.$http.post('/api/v1_0/uploadimage', {
                    type:'jpg',
                    data:this.result
                }).then(
                success => {
                    if(success.data.status=="0") {
                        that.isShow = true;
                        that.h5Img =success.data.url;
                        // console.log(that.h5Img)
                        that.$refs.formValidate.validateField("uploadimg")
                    }else {
                        that.$Modal.error({
                            title:'提示',
                            // content:'上传失败，请重试'
                            content: success.data.msg
                        })
                    }
                },
                error => {
                    // console.log(error)
                    this.$Modal.error({
                      title:'提示',
                      content:error.data.msg
                    })
                })
            }
        },
    }
}
</script>
<style lang="scss">
#ActivityList{
    height: 100%;
    padding: 20px;
    width: 100%;
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    .h1{
        font-size: 22px;
        color: #808080;
    }
    .header {
        margin-top: 20px;
        text-align: right;
        margin-bottom: 30px;
        position: relative;
        height: 42px;
        //新增按钮
        .newbtn {
            float: right;
            text-align: left;
            margin-left: 10px;
        }
        &:before,
        &:after {
            display: table;
            line-height: 0;
            content: "";
        }
        &:after {
            clear: both;
        }
    }
}
//新增编辑弹框
.ivu-radio-inner:after {
    position: absolute;
    width: 8px;
    height: 8px;
    left: 2px;
    top: 2px;
    border-radius: 6px;
    display: table;
    border-top: 0;
    border-left: 0;
    content: ' ';
    background-color: #ffc639 !important;
    opacity: 0;
    transition: all .2s ease-in-out;
    transform: scale(0);
}
.ma-edit-modal {
  .edit-modal-body {
    position: relative;
    margin-bottom: 30px;
    font-size: 14px
  }
  .ivu-icon-android-close {
    position: absolute;
    top: -20px;
    right: -14px;
    font-size: 24px;
    color: var(--base);
    cursor: pointer;
  }
  .title {
    margin-bottom: 24px;
    text-align: center;
    font-size: 24px;
    color: var(--base);
  }
    .ivu-radio-checked .ivu-radio-inner{
        border-color: var(--base) !important;
    }
  //弹框表单
  .edit-form {
    .error-tip {
      position: absolute;
      top: 100%;
      left: 0;
      line-height: 1;
      padding-top: 6px;
      color: #ed4958;
    }
    .role-select {
      height: 42px;
      line-height: 42px;
    }
    .department-select {
      margin-right: 12px;
    }
    .department-select,
    .job-select {
      width: 48%;
    }
  }
}
</style>
