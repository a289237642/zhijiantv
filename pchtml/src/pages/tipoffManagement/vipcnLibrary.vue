<template>
    <div id="tipoffLibrary">
       <div class="h1">公众号库       
          <!-- <div class="search">
              <Input v-model="words" search enter-button="搜索" @on-search="searchTipoff" placeholder="请输入搜索关键字"/>
          </div> -->
        </div>
            
         <div class="header">
           <!-- <DatePicker v-model="startDate" type="date" placeholder="开始日期" style="width: 120px;" @on-change="getStart"></DatePicker>
        至
        <DatePicker type="date" v-model="endDate" placeholder="结束日期" style="width:120px;"  @on-change="getEnd"></DatePicker>   
           <Select v-model="arcSource" style="width:100px;margin-right:270px" placeholder="全部来源" @on-change="getCate">
             <Option value="" >全部来源</Option>
            <Option v-for="item in articleSource" :value="item" :key="item">{{ item }}</Option>
          </Select> -->
            <Button class="newbtn zhijian-new-btn" type="primary" @click="showLinkModal()" >新增</Button>
            <Button class="newbtn1 zhijian-new-btn" type="primary" @click="uploadStatus1">批量设置</Button>
            <Button class="newbtn2 zhijian-new-btn" type="primary" @click="delectArcs">批量删除</Button>
        </div>    
       <Table class="zhijian-table account-table" stripe :columns="table.columns" :data="table.data" ref="selection"  @on-selection-change="onArc" @on-select-all="onlineArc"></Table>
        <div class="zhijian-pagination">
            <Page :total="table.total" :current="table.page" show-elevator @on-change="changePage" :pageSize="table.pagesize"></Page>
        </div>
       
        <!-- 设置公众号类型编辑框 -->
        <Modal :mask-closable="false" v-model="uploadModal" width="535" class-name="ma-upload-modal">
             <div class="edit-modal-body">
              <div class="title">请选择需要设置的类型</div>
               <Checkbox-group v-model="checkedGroup" v-for="item in groups" :key="item.groups" @on-change="checkMoreGroupChange">
                  <Checkbox  :label="item.group_id" >{{item.group_name}}</Checkbox>
               </Checkbox-group>
             </div>
             <div class="zhijian-btn-box">
                <div class="zhijian-btn-confirm" @click="editcategory">确定</div>
            </div>
        </Modal>
        <!--公众号新增  -->
        <Modal :mask-closable="false" v-model="addLinkModal" width="535" class-name="ma-edit-modal">
            <div class="edit-modal-body hint">
                <Icon type="android-close" @click="editModal=false"></Icon>
                <Form ref="formValidate1" :model="formValidate1" :rules="ruleValidate1" :label-width="120">
                   <FormItem label="抓取来源（名称）" prop="wechat_name">
                        <Input v-model="formValidate1.wechat_name" type="text"  placeholder="请输入抓取来源（名称）"></Input>
                    </FormItem>
                     <FormItem label="公众号ID" prop="alias">
                        <Input v-model="formValidate1.alias" type="text"  placeholder="请输入公众号ID"></Input>
                    </FormItem>
                 
                </Form>
            </div>
            <div class="zhijian-btn-box">
              <Button class="newbtn zhijian-new-btn" type="primary" @click="submitLinkForm('formValidate1')">确定</Button>
            </div>
             
        </Modal>
        
    </div>
</template>
<script>
import moment from "moment";
export default {
  name: "tipoffLibrary",
  data() {
    const validateImg = (rule, value, callback) => {
      if (this.h5Img == "") {
        callback(
          new Error("请上传公众号头图(大小不超过2M, 只支持jpg,jpeg,gif,bmp格式)")
        );
      } else {
        callback();
      }
    };
    return {
      uploadModal: false,
      addLinkModal: false,
      isDisable: true,
      h5Img: "",
      articleid_img: "",
      checkedGroup: [],
      groups: [],
      articleSource: [],
      articleid: "",
      isShow: false,
      onlineid: 0,
      art_detail: {},
      checkedArc: [], //批量处理
      table: {
        page: 1,
        pagesize: 10,
        total: 10,
        columns: [
          {
            type: "selection",
            title: "全选",
            width: 60,
            align: "center"
          },
           {
            title: "序号",
            width: 80,
            key:'location',
            align: "center"
          },
          {
            title: "抓取来源（名称）",
            // width: 500,
            key:'wechat_name',
            align: "center"
          },
          {
            title: "公众号ID",
            // width: 400,
            key:'alias',
            align: "center"
          },
          {
            title: "操作",
            align: "center",
            // width: 500,
            render: (h, params) => {
              return h("div", [
                h(
                  "i-button",
                  {
                    attrs: {
                      title: ""
                    },
                    style: {
                      marginRight: "10px"
                    },
                    on: {
                      click: () => {
                        this.checkedArc = [];
                        this.uploadStatus(params.row.wechat_id);
                      }
                    }
                  },
                  "设置"
                ),
                h(
                  "i-button",
                  {
                    on: {
                      click: () => {
                        this.$Modal.warning({
                          content: "确定删除该公众号吗?",
                          onOk: () => {
                            this.checkedArc = [];
                            this.deleteTipoff(params.row.wechat_id);
                          }
                        });
                      }
                    }
                  },
                  "删除"
                )
              ]);
            }
          }
        ],
        data: []
      },
      formValidate: {
        main_img: ""
      },
      ruleValidate: {
        uploadimg: [
          {
            required: true,
            validator: validateImg,
            trigger: "blur"
          }
        ]
      },
      formValidate1: {
        link: ""
      },
      ruleValidate1: {
        link: [
          { required: true, message: "请输入要抓取的公众号链接", trigger: "blur" }
        ]
      }
    };
  },
  methods: {
    //渲染公众号列表数据
    getData() {
      this.$http
        .post(this.PATH.WECHATNAMELIST, {
          page: this.table.page,
          pagesize: this.table.pagesize,
          is_show: 0
        })
        .then(res => {
          console.log(res.data.count);
          if (res.data.errno == 0) {
            this.table.data = res.data.data;
            this.table.total = res.data.count;
          } else {
            this.$Modal.error({
              width: 360,
              content: res.data.errmsg
            });
          }
        });
    },
    //分页
    changePage(page) {
      this.table.page = page;
      if (this.is_search) {
        // console.log("search");
        this.searchTipoff();
      } else {
        // console.log("no");
        this.getData();
      }
    },
   
    //添加公众号
    showLinkModal() {
      this.addLinkModal = true;
    },
    // 新增公众号
    submitLinkForm(name) {
      let content = this.formValidate1.content;
      this.$refs[name].validate(valid => {
        if (valid) {
          let type = this.formValidate1.type;
          let path = this.PATH.ADDWECHATNAME;
          let params = new Object();
          params = {
              wechat_name: this.formValidate1.wechat_name,
              alias: this.formValidate1.alias
            };
          this.$http.post(path, params).then(success => {
            console.log(success.data.errno);
            if(success.data.errno==0){
              this.$Modal.success({
                title: "提示",
                content: success.data.errmsg,
                onOk: () => {
                  this.addLinkModal = false;
                }
              });
                this.formValidate1.wechat_name = "";
                this.formValidate1.alias = "";
            }else{
              this.$Modal.success({
                title: "提示",
                content: success.data.errmsg,
                onOk: () => {
                  this.addLinkModal = false;
                }
              });
            }
            
            this.getData();
          });
        } else {
          this.$Message.error("Fail!");
        }
      });
    },
    //根据id删除某条公众号信息
    deleteTipoff(vipcnid) {
      let list = [];
      list.push(vipcnid);
      this.$http
        .post(this.PATH.DELWECHATNAME, {
          wechat_id_list: list
        })
        .then(res => {
          if (res.data.errno == 0) {
            this.getData();
          } else {
            this.$Modal.error({
              width: 360,
              content: res.data.errmsg
            });
          }
        });
    },
    // 批量删除
    delectArcs() {
      this.$Modal.warning({
        content: "确定删除该爆料吗?",
        onOk: () => {
          this.$http
            .post(this.PATH.DELWECHATNAME, {
              wechat_id_list: this.checkedArc
            })
            .then(res => {
              console.log(res.data.errmsg);
              if (res.data.errno == 0) {
                this.getData();
                this.checkedArc = [];
              } else {
                this.$Modal.error({
                  width: 360,
                  content: res.data.errmsg
                });
              }
            });
        }
      });
    },
   
    //获取设置类型
    getGroups() {
      //向后台请求上线类型数据
      this.$http.get(this.PATH.GROUPS).then(res => {
        if (res.data.errno == 0) {
          this.groups = res.data.data;
        } else {
          this.$Modal.error({
            width: 360,
            content: res.data.errmsg
          });
        }
      });
    },
    //设置公众号类型
    uploadStatus(vipcnid) {
      this.uploadModal = true;
      this.checkedArc.push(vipcnid);
      this.getGroups();
    },
    //设置公众号类型
    uploadStatus1() {
      this.uploadModal = true;
      this.getGroups();
    },
    // 全选拿到选中的公众号id
    onlineArc(selection) {
      this.checkedArc = [];
      selection.forEach(v => {
        this.checkedArc.push(v.wechat_id);
      });
      console.log(this.checkedArc, "全选");
    },
  
    // 多选拿到选中的公众号id
    onArc(selection) {
      this.checkedArc = [];
      selection.forEach(v => {
        this.checkedArc.push(v.wechat_id);
      });
      console.log(selection);
      console.log(this.checkedArc, "多选");
    },
    //多选选择的上线类型
    checkMoreGroupChange(data) {
      this.checkedGroup = data;
    },
    //修改公众号设置类型
    editcategory() {
      let arr = this.checkedGroup;
      this.$http
        .post(this.PATH.SETWECHATGROUP, {
          wechat_id_list: this.checkedArc,
          group_id_list: arr
        })
        .then(res => {
          console.log(res,'设置')
          if (res.data.errno == 0) {
            this.checkedArc = []; //清空多选公众号id
            this.getData(); //重新渲染
          } else {
            this.$Modal.error({
              width: 360,
              content: res.data.errmsg
            });
          }
          this.checkedGroup = []; //清空选中列表
          this.uploadModal = false; //隐藏模态框
        });
    },
    
  },
  //进入页面就渲染列表数据
  created() {
    this.getData();
    this.getGroups();
  }
};
</script>
<style lang="scss">
#tipoffLibrary {
  height: 100%;
  padding: 30px;
  width: 100%;
  margin-bottom: 20px;
  position: relative;
  box-sizing: border-box;
  -webkit-box-sizing: border-box;
  .edit-modal-body {
    .title {
      margin-bottom: 24px;
      text-align: center;
      font-size: 24px;
      color: var(--base);
    }
  }

  .h1 {
    font-size: 22px;
    color: #808080;
    margin-bottom: 20px;
  }
  .search {
    position: absolute;
    top: 82px;
    right: 160px;
  }
  .header {
    margin-top: 5px;
    text-align: right;
    margin-bottom: 35px;
    position: relative;
    height: 42px;
    //新增按钮
    .newbtn {
      float: right;
      text-align: left;
      margin-left: 10px;
    }
    .newbtn1 {
      float: left;
      text-align: left;
      margin-left: 10px;
    }
    .newbtn2 {
      float: left;
      text-align: left;
      margin-left: 10px;
    }
    .zhijian-new-btn {
      height: 32px;
      line-height: 10px;
    }
  }

  .content {
    img {
      margin-top: 10px;
    }
  }
  .hint {
    p {
      color: #ccc;
      text-align: center;
    }
  }

  .demo-spin-icon-load {
    animation: ani-demo-spin 1s linear infinite;
  }
  @keyframes ani-demo-spin {
    from {
      transform: rotate(0deg);
    }
    50% {
      transform: rotate(180deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
  .demo-spin-col {
    height: 100px;
    position: relative;
    border: 1px solid #eee;
  }
}
.detail {
  height: 600px;
  overflow: auto;
}
.detail h1 {
  font-size: 28px;
  font-weight: 700;
  text-align: left;
  width: 100%;
  box-sizing: border-box;
}
.detail .come-from {
  width: 100%;
  display: flex;
  font-size: 22px;
  color: #888d95;
  justify-content: space-between;
  margin-top: 30px;
}
.detail .cont-text {
  width: 100%;
  font-size: 20px;
  line-height: 2.5;
  color: #212121;
  line-height: 1.5;
  padding: 20px 0 30px 0;
  letter-spacing: 6px;
  font-weight: 400;
  text-indent: 2em;
}
.detail .cont-img {
  width: 100%;
}
</style>
