<template>
  <div id="keywordsManagement">
    <div class="h1">文章标签管理
      <!-- <div class="search">
        <Input v-model="words" search enter-button="搜索" @on-search="search" placeholder="请输入搜索关键字"/>
      </div>-->
    </div>

    <div class="header">
      <Button class="newbtn zhijian-new-btn" type="primary" @click="showEditModal('new')">新增</Button>
    </div>
    <Table class="zhijian-table account-table" stripe :columns="table.columns" :data="table.data"></Table>
    <div style="margin: 10px;overflow: hidden">
      <div style="float: right;">
        <Page
          :total="table.total"
          :current="table.page"
          show-elevator
          :pageSize="table.pagesize"
          @on-change="changePage"
        ></Page>
      </div>
    </div>

    <Modal :mask-closable="false" v-model="editModal" width="535" class-name="ma-edit-modal">
      <div class="edit-modal-body">
        <Icon type="android-close" @click="editModal=false"></Icon>
        <div v-if="formValidate.type=='new'" class="title">新增标签</div>
        <div v-if="formValidate.type=='edit'" class="title">编辑标签</div>
        <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="100">
          <FormItem v-if="arcCateList.length != 0" label="文章爆料类型" prop="arcCate">
            <Select v-model="formValidate.arcCate">
              <Option
                v-for="item in arcCateList"
                :value="item.group_id"
                :key="item.group_id"
              >{{ item.group_name }}</Option>
            </Select>
          </FormItem>
          <FormItem label="一级关键词" prop="first_keywords">
            <Input
              v-model="formValidate.first_keywords"
              autosize
              type="textarea"
              placeholder="关键词之间请用逗号隔开"
            ></Input>
          </FormItem>
          <FormItem label="二级属性词" prop="second_keywords">
            <Input
              v-model="formValidate.second_keywords"
              autosize
              type="textarea"
              placeholder="关键词之间请用逗号隔开"
            ></Input>
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
  name: "keywordsManagement",
  data() {
    return {
      editModal: false,
      arcCateList: [],

      table: {
        page: 1,
        pagesize: 10,
        total: 50,
        editgroupId: 0,
        columns: [
          {
            title: "序号",
            key: "location",
            width: 130,
            align: "center"
          },
          {
            title: "爆料类型名称",
            key: "article_group_name",
            align: "center"
          },
          {
            title: "一级关键词",
            key: "first_keywords",
            align: "center"
          },
          {
            title: "二级属性词",
            key: "second_keywords",
            align: "center"
          },
          {
            title: "操作",
            align: "center",
            render: (h, params) => {
              return h("div", [
                h("i", {
                  attrs: {
                    class: "iconfont icon-edit"
                  },
                  on: {
                    click: () => {
                      this.showEditModal("edit", params.row);
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
                      this.$Modal.confirm({
                        content: "确定删除吗?",
                        onOk: () => {
                          this.$http
                            .post(this.PATH.DELKEYWORD, {
                              keywords_id_list: [params.row.keyword_id]
                            })
                            .then(res => {
                              if (res.data.errno === 0) {
                                console.log("shanchu");
                                this.getKeywordList(1, 10);
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
      formValidate: {
        type: "new",
        row: {},
        first_keywords: "",
        second_keywords: "",
        arcCate: ""
      },
      ruleValidate: {
        arcCate: [
          {
            required: true,
            message: "请选择爆料类型",
            trigger: "blur",
            type: "number"
          }
        ],
        first_keywords: [
          { required: true, message: "请输入一级关键词", trigger: "blur" }
        ],
        second_keywords: [
          { required: true, message: "请输入二级属性词", trigger: "blur" }
        ]
      }
    };
  },
  methods: {
    //获取跳转爆料类别
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
    },
    //获取标签列表
    getKeywordList(page, pagesize) {
      this.$http
        .post(this.PATH.KEYWORDLIST, {
          page,
          pagesize
        })
        .then(res => {
          console.log(res.data.data);
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
    /**
     * 分页
     */
    changePage(page) {
      console.log(page);
      this.table.page = page;
      this.getKeywordList(page, this.table.pagesize);
    },

    showEditModal(type, row) {
      // 显示添加爆料类型
      this.formValidate.type = type;
      if (type == "new") {
        this.getgroups();
        //对整个表单进行重置，将所有字段值重置为空并移除校验结果
        this.$refs.formValidate.resetFields();
        this.formValidate.arcCate = "";
        this.formValidate.group_id = "";
        this.formValidate.content = "";
        this.formValidate.sort = "";
      } else {
        this.arcCateList = [];
        this.formValidate.group_id = row.article_group_id;
        this.formValidate.keyword_id = row.keyword_id;
        this.formValidate.first_keywords = row.first_keywords;
        this.formValidate.second_keywords = row.second_keywords;
      }
      this.editModal = true;
    },
    //提交表单数据给后台
    submitForm(name) {
      this.$refs[name].validate(valid => {
        if (valid) {
          let type = this.formValidate.type;
          let path;
          let params = new Object();
          if (type == "new") {
            path = this.PATH.KEYWORDADD;
            params = {
              article_group_id: this.formValidate.arcCate,
              first_keywords: this.formValidate.first_keywords,
              second_keywords: this.formValidate.second_keywords
            };
          } else {
            path = this.PATH.KEYWORDUPLOAD;
            params = {
              article_group_id: this.formValidate.group_id,
              keyword_id: this.formValidate.keyword_id,
              first_keywords: this.formValidate.first_keywords,
              second_keywords: this.formValidate.second_keywords
            };
          }
          this.$http.post(path, params).then(res => {
            console.log(res);
            if (res.data.errno === 0) {
              this.editModal = false;
              this.getKeywordList(1, 10);
            }
          });
        } else {
          this.$Message.error("Fail!");
        }
      });

      // let type = this.formValidate.type;
      // let path;
      // let params = new Object();
      // if (type == "new") {
      //   path = this.PATH.KEYWORDADD;
      //   params = {
      //     article_group_id: this.formValidate.arcCate,
      //     first_keywords: this.formValidate.first_keywords,
      //     second_keywords: this.formValidate.second_keywords
      //   };
      // } else {
      //   path = this.PATH.KEYWORDUPLOAD;
      //   params = {
      //     article_group_id: this.formValidate.group_id,
      //     keyword_id: this.formValidate.keyword_id,
      //     first_keywords: this.formValidate.first_keywords,
      //     second_keywords: this.formValidate.second_keywords
      //   };
      // }
      // this.$http.post(path, params).then(res => {
      //   console.log(res);
      //   if (res.data.errno === 0) {
      //     this.editModal = false;
      //     this.getKeywordList(1, 10);
      //   }
      // });
    }
  },

  created() {
    this.getKeywordList(1, 10);
  }
};
</script>
<style lang="scss">
#keywordsManagement {
  height: 100%;
  padding: 20px;
  width: 100%;
  box-sizing: border-box;
  -webkit-box-sizing: border-box;
  .h1 {
    font-size: 22px;
    color: #808080;
    margin-bottom: 20px;
  }
  .search {
    width: 200px;
    position: absolute;
    top: 132px;
    right: 160px;
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
    .zhijian-new-btn {
      height: 32px;
      line-height: 12px;
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
}
</style>
