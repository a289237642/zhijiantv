<template>
    <div id="tipoffManagement">
       <div class="h1">爆料类型管理
         <div class="search">
                <Input v-model="words" search enter-button="搜索" @on-search="search" placeholder="请输入搜索关键字"/>
          </div>
       </div>
        
        <div class="header">
            <Button class="newbtn zhijian-new-btn" type="primary" @click="showEditModal('new')">新增</Button>
        </div>
        <Table class="zhijian-table account-table" stripe :columns="table.columns" :data="table.data"></Table>
         <Modal :mask-closable="false" v-model="editModal" width="535" class-name="ma-edit-modal">
            <div class="edit-modal-body">
                <Icon type="android-close" @click="editModal=false"></Icon>
                <div v-if="formValidate.type=='new'" class="title">新增爆料类型</div>
                <div v-if="formValidate.type=='edit'" class="title">编辑爆料类型</div>
                <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="100">
                   <FormItem label="排序" prop="sort">
                        <Input v-model="formValidate.sort" type="text"  placeholder="Enter something..."></Input>
                    </FormItem>
                    <FormItem label="爆料类型名称" prop="content">
                        <Input v-model="formValidate.content" type="text"  placeholder="Enter something..."></Input>
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
  name: "tipoffManagement",
  data() {
    return {
      editModal: false,
      words: "",
      table: {
        page: 1,
        pagesize: 10,
        total: 50,
        editgroupId: 0,
        columns: [
          {
            title: "排序",
            key: "sort_num",
            width: 130,
            align: "center"
          },
          {
            title: "爆料类型ID",
            key: "group_id",
            width: 130,
            align: "center"
          },
          {
            title: "爆料类型名称",
            key: "group_name",
            align: "center"
          },
          {
            title: "操作",
            align: "center",
            render: (h, params) => {
              return h("div", [
                h("i-switch", {
                  attrs: {
                    title: params.row.is_show == "0" ? "已停用" : "已启用"
                  },
                  props: {
                    value: params.row.is_show + "", //这个值是字符串类型
                    trueValue: "1",
                    falseValue: "0"
                  },
                  on: {
                    "on-change": value => {
                      this.changeStatus(
                        params.row.group_id,
                        params.row._index,
                        value
                      );
                    }
                  }
                }),
                h("i", {
                  attrs: {
                    class: "iconfont icon-edit"
                  },
                  on: {
                    click: () => {
                      this.showEditModal("edit", params.row);
                      this.table.editgroupId = params.row.group_id;
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
                        content: "确定删除该爆料类型吗?",
                        onOk: () => {
                          this.$http
                            .post(this.PATH.DELGROUP, {
                              group_id: params.row.group_id.slice(2)
                            })
                            .then(res => {
                              if (res.status == 200) {
                                this.getgroups();
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
        content: "",
        sort: ""
      },
      ruleValidate: {
        sort: [{ required: true, message: "序号", trigger: "blur" }],
        content: [
          { required: true, message: "请输入爆料类型名称", trigger: "blur" }
        ]
      }
    };
  },
  methods: {
    //获取爆料类型列表
    getgroups() {
      this.$http.get(this.PATH.PCGROUPS).then(res => {
        console.log(res.data.data);
        if (res.data.errno == 0) {
          this.table.data = res.data.data;
        } else {
          this.$Modal.error({
            width: 360,
            content: res.data.errmsg
          });
        }
      });
    },
    //搜索功能
    search() {
      if(this.words == ""){
        this.getgroups();
      }else{
        this.$http
        .post(this.PATH.GROUPSEARCH, {
          words: this.words
        })
        .then(res => {
          console.log(res);
          if (res.data.errno == 0) {
            this.table.data = res.data.data;
          } else {
            this.$Modal.error({
              width: 360,
              content: res.data.errmsg
            });
          }
        });
      }
      this.words = ""; //搜索完成清空
    },
    // 开启、停用爆料类型
    changeStatus(id, index, nValue) {
      let msg = "该爆料类型已开启";
      if (nValue == "0") {
        msg = "该爆料类型已停止使用";
      }
      id = id.slice(2);
      this.$http
        .post(this.PATH.STARTGROUP, {
          group_id: id
        })
        .then(res => {
          if (res.status == "200") {
            this.table.data[index].is_show = nValue;
          } else {
            //如果发请求失败，状态回滚：
            this.table.data[index].is_show = nValue == "1" ? "0" : "1";
            this.$Modal.error({
              width: 360,
              content: res.data.msg
            });
          }
          this.getgroups(); //修改完状态后重新渲染
        });
    },
    showEditModal(type, row) {
      // 显示添加爆料类型
      this.formValidate.type = type;
      if (type == "new") {
        //对整个表单进行重置，将所有字段值重置为空并移除校验结果
        this.$refs.formValidate.resetFields();
        this.formValidate.group_id = "";
        this.formValidate.content = "";
        this.formValidate.sort = "";
      } else {
        this.formValidate.group_id = row.group_id;
        this.formValidate.content = row.group_name;
        this.formValidate.sort = row.sort_num;
      }
      this.editModal = true;
    },
    //提交表单数据给后台
    submitForm(name) {
      let content = this.formValidate.content;
      this.$refs[name].validate(valid => {
        if (valid) {
          let type = this.formValidate.type;
          let path = this.PATH.UODATEGROUP;
          let params = new Object();
          if (type == "new") {
            params = {
              name: content,
              sort_num: this.formValidate.sort
            };
          } else {
            params = {
              name: content,
              group_id: this.table.editgroupId.slice(2),
              sort_num: this.formValidate.sort
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
            this.getgroups();
          });
        } else {
          this.$Message.error("Fail!");
        }
      });
    }
  },

  created() {
    this.getgroups();
  }
};
</script>
<style lang="scss">
#tipoffManagement {
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
