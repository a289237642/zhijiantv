<template>
  <div id="tipoffList">
    <div class="h1">24小时热榜</div>
    <!-- 新增 -->
    <div class="header">
      <Button class="newbtn zhijian-new-btn" type="primary" @click="showEditModal('new')">新增</Button>
    </div>
    <Table
      border
      class="zhijian-table account-table"
      :row-class-name="rowClassName"
      :columns="table.columns"
      :data="table.data"
    ></Table>
    <div class="zhijian-pagination">
      <Page
        :total="table.total"
        :current="table.page"
        show-elevator
        @on-change="changePage"
        :pageSize="table.pagesize"
      ></Page>
    </div>
    <!-- 新增、编辑弹框 -->
    <Modal :mask-closable="false" v-model="editModal" width="535" class-name="ma-edit-modal">
      <div class="edit-modal-body">
        <Icon type="android-close" @click="editModal=false"></Icon>
        <div v-if="formValidate.type=='new'" class="title">24小时热榜新增</div>
        <div v-if="formValidate.type=='edit'" class="title">24小时热榜编辑</div>
        <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="100">
          <FormItem label="请输入内容" prop="content">
            <Input
              v-model="formValidate.content"
              type="textarea"
              :autosize="{minRows: 2,maxRows: 5}"
              placeholder="Enter something..."
            ></Input>
          </FormItem>
          <FormItem label="排序" prop="sort">
            <Input v-model="formValidate.sort" placeholder="请输入排序号"></Input>
          </FormItem>
          <FormItem label="跳转文章类型" prop="articlecategory">
            <Select v-model="arcCate" @on-change="getArticle">
              <Option value>请选择</Option>
              <Option
                v-for="item in arcCateList"
                :value="item.group_id"
                :key="item.group_id"
              >{{ item.group_name }}</Option>
            </Select>
          </FormItem>
          <FormItem label="选择跳转文章" prop="article" placeholder="请先选择跳转文章类型">
            <Select
              v-model="arcId"
              value-key="article"
              @on-change="searchArc"
              :label-in-value="true"
            >
              <Option
                v-for="item in arcList"
                :value="item.article_id"
                :key="item.article_id"
              >{{ item.title }}</Option>
            </Select>
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
  name: "tipoffList",
  data() {
    return {
      hideIndex: [],
      arcCate: "",
      arcCateList: [],
      arcId: "",
      arcList: [],
      table: {
        page: 1,
        pagesize: 10,
        total: 50,
        editTopId: "",
        columns: [
          {
            title: "排序",
            key: "sort_num",
            align: "center"
          },
          {
            title: "内容",
            key: "content",
            align: "center"
          },
          {
            title: "创建时间",
            key: "create_time",
            align: "center",
            sortable: true
          },
          {
            title: "跳转文章",
            key: "jump_article_title",
            align: "center",
            sortable: true
          },
          {
            title: "操作",
            align: "center",
            render: (h, params) => {
              let className = this.table.className;
              return h("div", [
                h("i", {
                  attrs: {
                    class:
                      params.row.is_show == 0
                        ? "iconfont icon-yanjing-bi"
                        : "iconfont icon-yanjing"
                  },
                  on: {
                    click: () => {
                      this.$http
                        .post(this.PATH.UPLOADTOP, {
                          top_id: params.row.top_id,
                          is_show: params.row.is_show
                        })
                        .then(res => {
                          if (res.status == 200) {
                            this.getData();
                          }
                        });
                    }
                  }
                }),
                h("i", {
                  attrs: {
                    class: "iconfont icon-edit"
                  },
                  on: {
                    click: () => {
                      this.formValidate.row = params.row;
                      this.formValidate.type = "edit";
                      this.getgroups();
                      this.getArticle1(params.row);
                      // this.showEditModal("edit", params.row);
                    }
                  }
                }),
                h("i", {
                  attrs: {
                    class: "iconfont icon-delete"
                  },
                  style: {
                    color: "#ffc639"
                  },
                  on: {
                    click: () => {
                       this.$Modal.warning({
                          content: "确定删除该热榜吗?",
                          onOk: () => {
                           this.$http
                            .post(this.PATH.DELTOP, {
                              top_id: params.row.top_id
                            })
                            .then(res => {
                              console.log(res);
                              if (res.status == 200) {
                                  this.$Modal.success({
                                  width: 360,
                                  content: res.data.errmsg,
                                });
                                this.getData();
                              }
                            });
                          }
                        });
                      
                    }
                  }
                })
              ]);
            }
          }
        ],
        data: []
      },
      editModal: false,
      formValidate: {
        type: "new",
        row: {},
        content: ""
      },
      ruleValidate: {
        content: [
          { required: true, message: "请输入热榜内容", trigger: "blur" }
        ]
      }
    };
  },
  created() {
    this.getData();
  },
  methods: {
    getData() {
      this.$http
        .post(this.PATH.PCTOPS, {
          page: this.table.page,
          pagesize: this.table.pagesize
        })
        .then(res => {
          console.log(res);
          if (res.status == 200) {
            if (res.data.errno == 0) {
              this.table.data = res.data.data;
              this.table.total = res.data.count;
            } else {
              this.$Modal.error({
                width: 360,
                content: res.data.errmsg
              });
            }
          }else {
          this.$Message.error("Fail!");
        }
        });
    },
    //展示弹框
    showEditModal(type, row) {
      // console.log(row);
      this.getgroups();
      // 显示添加分组、编辑
      this.formValidate.type = type;
      if (type == "new") {
        //对整个表单进行重置，将所有字段值重置为空并移除校验结果
        this.$refs.formValidate.resetFields();
        this.arcCate = "";
        this.arcId = "";
        this.arcList = [];
        this.arcCateList = [];
      } else {
        console.log(row);
        // this.getArticle(row.jump_article_group_id);
        this.table.editTopId = row.top_id;
        this.formValidate.content = row.content;
        this.formValidate.sort = row.sort_num;
        this.arcCate = row.jump_article_group_id;
        this.arcId = row.jump_article_id;
      }
      this.editModal = true;
    },
    // 隐藏弹框
    // closeModal(){
    //   this.arcCate = "";
    //   this.arcId = "";
    // },
    getArticle(value) {
      console.log(222);
      this.arcCate = value; //拿到要跳转的文章类型ID
      if (this.arcCate == "") {
        return;
      } else {
        this.$http
          .post(this.PATH.ARTICLEGROUP, {
            group_id: this.arcCate,
            pagesize: 100
          })
          .then(res => {
            console.log(res.data);
            if (res.status == 200) {
              this.arcList = res.data.data;
            }
          });
      }
    },
     getArticle1(row) {
      console.log(row);
      this.arcCate = row.jump_article_group_id; //拿到要跳转的文章类型ID
        this.$http
          .post(this.PATH.PCARTICLETITLE, {
            group_id: this.arcCate
          })
          .then(res => {
            console.log(res.data);
            if (res.status == 200) {
              this.arcList = res.data.data;
              this.editModal = true;
              this.table.editTopId = row.top_id;
              this.formValidate.content = row.content;
              this.formValidate.sort = row.sort_num;
              this.arcCate = row.jump_article_group_id;
              this.arcId = row.jump_article_id;
              
            }
          });
      },

    searchArc(query) {
      console.log(query);
      this.arcId = query.value; //选择跳转文章的ID
      this.formValidate.content = query.label;//文章标题
    },
    rowClassName(row, index) {
      let className = this.table.className;
      if (row.is_show == 0) {
        return "hide-table-row";
      }
      return "";
    },
    submitForm(name) {

      let content = this.formValidate.content;
      let editTopId = this.table.editTopId;
      console.log(editTopId,this.formValidate.type,'edit');
      this.$refs[name].validate(valid => {
        if (valid) {
          let type = this.formValidate.type;
          let path = this.PATH.ADDTOP;
          let params = new Object();
          if (type == "new") {
            params = {
              content: content,
              sort_num: this.formValidate.sort,
              article_id: this.arcId,
              group_id: this.arcCate
            };
          } else {
            params = {
              content: content,
              top_id: editTopId,
              sort_num: parseInt(this.formValidate.sort),
              article_id: this.arcId,
              group_id: this.arcCate
            };
          }
          this.$http.post(path, params).then(success => {
            if (this.formValidate.type == "new") {
              this.$Modal.success({
                title: "提示",
                content: success.data.errmsg,
                onOk: () => {
                  this.editModal = false;
                }
              });
            } else {
              this.$Modal.success({
                title: "提示",
                content: success.data.errmsg,
                onOk: () => {
                  this.editModal = false;
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
    changePage(page) {
      this.table.page = page;
      this.getData();
    },
    //获取跳转文章类别
    getgroups() {
      this.$http.get(this.PATH.GROUPS).then(res => {
        console.log(res);
        if (res.data.errno == 0) {
          this.arcCateList = res.data.data;
        } else {
          this.$Modal.error({
            width: 360,
            content: res.data.errmsg
          });
        }
      });
    }
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
  .h1 {
    font-size: 22px;
    color: #808080;
  }
  .account-table {
    margin-top: 20px;
  }
  .header {
    margin-top: 20px;
    text-align: right;
    margin-bottom: 40px;
    position: relative;
    height: 60px;
    //新增按钮
    .newbtn {
      float: right;
      text-align: left;
      margin-left: 10px;
    }
  }
}
//新增编辑弹框
.ma-edit-modal {
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
  .title {
    margin-bottom: 24px;
    text-align: center;
    font-size: 24px;
    color: var(--base);
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
