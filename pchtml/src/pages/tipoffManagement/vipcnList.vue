<template>
    <div id="tipoffList">
        <h1>公众号列表</h1>
        
        <Button class="newbtn zhijian-new-btn" type="primary" @click="downline1" >批量重置</Button>
         <Tabs :value="name0" @on-click="handTabClick" >
            <TabPane label="全部" name="name0">
                <Table class="tip-table" border :columns="columns2" :data="data2" ref="selection"  @on-selection-change="downArc" @on-select-all="downlineArc"></Table>
                <div class="zhijian-pagination">
                    <Page :total="table.totalAll" :current="table.page" show-elevator @on-change="changePageAll" :pageSize="table.pagesize"></Page>
                </div>
            </TabPane>
            <TabPane :label="item.group_name" :name="item.group_id + ''"  v-for="item in onlinelist" :value="item.group_id" :key="item.group_id" >
              
                <Table class="tip-table" border :columns="columns1" :data="data1" ref="selection"  @on-selection-change="downArc" @on-select-all="downlineArc"></Table>
                <div class="zhijian-pagination">
                    <Page :total="table.total" :current="table.page" show-elevator @on-change="changePage" :pageSize="table.pagesize"></Page>
                </div>
                
            </TabPane>
        </Tabs>
         <Modal v-model="modal1" title="Common Modal dialog box title">
            <p class="modelp">请确认该公众号重置</p>
            <div class="zhijian-btn-box">
                <div class="zhijian-btn-confirm" @click="ok">确定</div>
            </div>
        </Modal>
        <Modal v-model="modal" title="Common Modal dialog box title">
            <p class="modelp">请确认该公众号重置</p>
            <div class="zhijian-btn-box">
                <div class="zhijian-btn-confirm" @click="ok1">确定</div>
            </div>
        </Modal>
    </div>
</template>
<script>
export default {
  name: "tipoffList",
  data() {
    return {
      name0: "name0",
      paramses: {},
      modal1: false,
      modal:false,
      value: "",
      group_id: 1,
      groupidname:'',
      onlinelist: [],
      online: [],
      checkedArc: [], //批量设置
      table: {
        total: 10,
        totalAll: 10,
        totalSearch: 10,
        page: 1,
        pagesize: 10,
        is_show: 1
      },
      formValidate: {
        sort: "",
        onlinecategory: ""
      },
      ruleValidate: {
        sort: [{ required: true, message: "序号", trigger: "blur" }],
        content: [
          { required: true, message: "请选择上线类型", trigger: "blur" }
        ]
      },
      columns1: [
       {
            type: "selection",
            title: "全选",
            width: 60,
            align: "center"
          },
           {
            title: "序号",
            // width: 80,
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
            // width: 300,
            key:'alias',
            align: "center"
          },
        {
            title: "操作",
            align: "center",
            // width: 600,
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
                        this.paramses = params;
                        this.checkedArc.push(params.row.wechat_id);
                        console.log(params,'params.row.wechat_id');
                        this.modal1 = true;
                      }
                    }
                  },
                  "重置"
                )
              ]);
            }
          }
        ],
         columns2: [
       {
            type: "selection",
            title: "全选",
            width: 60,
            align: "center"
          },
           {
            title: "序号",
            // width: 80,
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
            // width: 300,
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
                        this.paramses = params;
                        this.checkedArc.push(params.row.wechat_id);
                        console.log(params,'222');
                        this.modal = true;
                      }
                    }
                  },
                  "重置"
                )
              ]);
            }
          }
        ],
      data1: [],
      data2: []
    };
  },
  created() {
    this.getgroups();
    this.getArticlesAll();
  },
  methods: {
     getArticlesAll() {
      this.$http
        .post(this.PATH.WECHATNAMELIST, {
          page: this.table.page,
          pagesize: this.table.pagesize,
          is_show: 1
        })
        .then(res => {
          console.log(res);
          if (res.status == 200) {
            this.data2 = res.data.data;
            this.table.totalAll = res.data.count;
          }
        });
    },
    // 获取分类公众号
    getArticles() {
      console.log(this.groupidname);
      this.$http
        .post(this.PATH.WECHATNAMEGROUP, {
          group_id: this.groupidname,
          page: this.table.page,
          pagesize: this.table.pagesize
        })
        .then(res => {
          console.log(res);
          if (res.status == 200) {
            this.data1 = res.data.data;
            this.table.total = res.data.count;
          }
        });
    },
    //切换tab栏
    handTabClick(groupid) {
      this.name0 = groupid;
      console.log(groupid);
      this.is_search = false;
      this.groupidname = groupid;
      this.changePages();
      if(groupid == 'name0'){
        this.getArticlesAll();
      }else{
        this.getArticles();
      }
    },
    // 全选拿到选中的文章id
    downlineArc(selection) {
      this.checkedArc = [];
      selection.forEach(v => {
        this.checkedArc.push(v.wechat_id);
      });
      // console.log(this.checkedArc,'全选');
    },
    // 多选拿到选中的文章id
    downArc(selection) {
      this.checkedArc = [];
      selection.forEach(v => {
        this.checkedArc.push(v.wechat_id);
      });
      console.log(this.checkedArc,'多选');
    },
    //批量设置
    downline1() {
      let paramss = {};
      let list = this.checkedArc;
        paramss = {
          wechat_id_list: list,
          group_id: this.groupidname
        };
      this.$http.post(this.PATH.RESETWECHATGROUP, paramss).then(res => {
        console.log(res.data.errmsg);
        if (res.status == 200) {
          this.getArticles();
          this.checkedArc = [];
        }
      });
    },
    // 操作下线
    downline() {
      console.log(this.paramses);
      let paramses = this.paramses;
      let paramss = {};
      let list = this.checkedArc;
      paramss = {
         wechat_id_list: list,
          group_id: this.groupidname
      };
      this.$http.post(this.PATH.RESETWECHATGROUP, paramss).then(res => {
        console.log(res);
        if (res.status == 200) {
          this.getArticles();
          this.checkedArc = [];
        }
      });
    },
    
    ok() {
      this.modal1 = false;
      this.downline();
    },
    // 全部 重置功能
      ok1() {
      this.modal = false;
       console.log(this.paramses);
      let paramses = this.paramses;
      let paramss = {};
      let list = this.checkedArc;
      paramss = {
         wechat_id_list: list
      };
      this.$http.post(this.PATH.RESETWECHATGROUP, paramss).then(res => {
        console.log(res);
        if (res.status == 200) {
          this.getArticlesAll();
          this.checkedArc = [];
        }
      });
    },
    changePages() {
      this.table.page = 1;
    },
  
    changePage(page) {
      this.table.page = page;
      this.getArticles();
    },
    changePageAll(page) {
      this.table.page = page;
      this.getArticlesAll();

    },
    getgroups() {
      this.$http.get(this.PATH.PCGROUPS).then(res => {
        if (res.data.errno == 0) {
        
          this.onlinelist = res.data.data.map(function(item) {
            return {
              group_id: parseInt(item.group_id.slice(2)), //把分类ID处理成数字
              group_name: item.group_name
            };
          });
            this.groupidname = this.onlinelist[0].group_id;
            console.log(this.groupidname,'this.groupidname')
            this.getArticles();
        } else {
          this.$Modal.error({
            width: 360,
            content: res.data.errmsg
          });
        }
      });
    },
  }
};
</script>
<style lang="scss">
#tipoffList {
  height: 100%;
  padding: 20px;
  width: 100%;
  box-sizing: border-box;
  -webkit-box-sizing: border-box;
  background: #fff;
  position: relative;
  h1 {
    font-size: 22px;
    color: #808080;
    margin-bottom: 30px;
  }
  .tip-table {
    margin: 0 30px;
    box-sizing: border-box;
  }
  .search {
    width: 200px;
    position: absolute;
    top: 20px;
    right: 20px;
  }
  .ivu-modal-footer {
    display: block;
  }
  .newbtn {
    position: absolute;
    top: 64px;
    right: 20px;
  }
  .newbtn1 {
    position: absolute;
    top: 64px;
    right: 130px;
  }
  .zhijian-new-btn {
    height: 32px;
    line-height: 10px;
    padding: 10px 10px;
  }
  //弹框
  .ma-edit-modal {
    .config {
      margin-bottom: 24px;
      text-align: center;
      font-size: 24px;
      color: var(--base);
    }
    .edit-modal-body {
      position: relative;
      margin-bottom: 30px;
      font-size: 14px;
    }
    .ivu-icon-android-close {
      position: absolute;
      top: -20px;
      right: -14px;
      font-size: 24px;
      color: var(--base);
      cursor: pointer;
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
}
.modelp {
  padding: 20px 0px;
  text-align: center;
  font-size: 16px;
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
.demo-spin-icon-load {
  animation: ani-demo-spin 1s linear infinite;
}
</style>
