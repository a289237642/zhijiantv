<template>
  <div id="typeManagement">
    <div class="h1">课程类型管理</div>
    <div class="header">
      <Button class="newbtn zhijian-new-btn" type="primary" @click="showEditModal('new')">新增</Button>
    </div>
    <Table class="zhijian-table account-table" stripe :columns="table.columns" :data="table.data"></Table>
    <div class="zhijian-pagination">
      <Page :total="table.total" :current="table.page" show-elevator @on-change="changePage" :pageSize="table.pagesize"></Page>
    </div>
    <Modal :mask-closable="false" v-model="editModal" width="535" class-name="ma-edit-modal">
      <div class="edit-modal-body">
        <Icon type="android-close" @click="editModal=false"></Icon>
        <div v-if="formValidate.type=='new'" class="title">新增类型</div>
        <div v-if="formValidate.type=='edit'" class="title">编辑类型</div>
        <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="100">
          <FormItem label="排序" prop="sort">
            <Input v-model="formValidate.sort" type="text"  placeholder="Enter something..."></Input>
          </FormItem>
          <FormItem label="类型名称" prop="content">
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
    name: "typeManagement",
    data() {
      return {
        editModal: false,
        table: {
          page: 1,
          pagesize: 10,
          total: 0,
          editgroupId: 0,
          columns: [
            {
              title: "序号",
              key: "sort",
              width: 130,
              align: "center"
            },
            {
              title: "课程ID",
              key: "type_id",
              width: 130,
              align: "center"
            },
            {
              title: "类型名称",
              key: "name",
              align: "center"
            },
            {
              title: "操作",
              align: "center",
              render: (h, params) => {
                return h("div",{
                  style:{
                    display:params.row.is_show == "2" ? 'none':'inline-block'
                    }
                }, [
                  h("i-switch", {
                    attrs: {
                      title: params.row.is_show == "0" ? "未上架" : "已上架"
                    },
                    props: {
                      value: params.row.is_show + "", //这个值是字符串类型
                      trueValue: "1",
                      falseValue: "0"
                    },
                    on: {
                      "on-change": value => {
                        this.changeStatus(
                          params.row.type_id,
                          value
                        );
                      }
                    }
                  }),
                  /*h(
                    "Button",
                    {
                      props: {
                        type: "primary",
                        size: "small",
                        class: "btn"
                      },
                      style: {
                        display: params.row.is_show == "0" ? "none" : "inline-block",
                        marginLeft: '10px'
                      },
                      on: {
                        click: () => {

                        }
                      }
                    },
                    params.row.is_show == "0" ? "" : "上移"
                  ),*/
                  h("i", {
                    attrs: {
                      class: "iconfont icon-edit"
                    },
                    on: {
                      click: () => {
                        this.showEditModal("edit", params.row);
                        this.table.editgroupId = params.row.type_id;
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
                               .post(this.PATH.DELETE_LESSON_TYPE, {
                                 type_id: params.row.type_id
                               })
                               .then(res => {
                                 if (res.data.errno === 0) {
                                   this.getSubject('z')
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
          sort: "",
        },
        ruleValidate: {
          sort: [{ required: true, message: "序号", trigger: "blur" }],
          content: [
            { required: true, message: "请输入类型名称", trigger: "blur" }
          ]
        }
      };
    },
    methods: {
      changePage(page) {
        this.table.page = page
        this.getSubject()
      },
      getSubject(_a) {
        let data = {}
        if (_a) {
          data = {
            page: 1,
            pagesize: 10
          }
        } else {
          data = {
            page: this.table.page,
            pagesize: this.table.pagesize
          }
        }
        this.$post(this.PATH.GET_LESSON_TYPE,data).then(res => {
          console.log(res);
          if (res.data.errno == 0) {
            this.table.total = res.data.count
            this.table.data = res.data.data
          } else {
            this.$Modal.error({
              width: 360,
              content: res.data.errmsg
            });
          }
        });
      },
      // 开启、停用爆料类型
      changeStatus(id, nValue) {
        let msg = "已开启";
        if (nValue == "0") {
          msg = "已停止使用";
        }
        this.$http
          .post(this.PATH.STATUS_LESSON_TYPE, {
            type_id: id
          })
          .then(res => {
            if (res.data.errno === 0) {
              this.getSubject(); //修改完状态后重新渲染
            } else {
              //如果发请求失败，状态回滚：
              this.getSubject(); //修改完状态后重新渲染
              // this.table.data[index].is_show = nValue == "1" ? "0" : "1";
              this.$Modal.error({
                width: 360,
                content: res.data.msg
              });
            }

          });
      },
      showEditModal(type, row) {
        // 显示添加爆料类型
        this.formValidate.type = type;
        if (type == "new") {
          //对整个表单进行重置，将所有字段值重置为空并移除校验结果
          this.$refs.formValidate.resetFields();
          this.formValidate.type_id = "";
          this.formValidate.content = "";
          this.formValidate.sort = "";
        } else {
          this.formValidate.type_id = row.type_id;
          this.formValidate.content = row.name;
          this.formValidate.sort = row.sort.toString();
        }
        this.editModal = true;
      },
      //提交表单数据给后台
      submitForm(name) {
        let content = this.formValidate.content;
        this.$refs[name].validate(valid => {
          if (valid) {
            let type = this.formValidate.type;
            let path
            let params = new Object();
            if (type == "new") {
              path = this.PATH.ADD_LESSON_TYPE;
              params = {
                name: content,
                sort: this.formValidate.sort
              };
            } else {
              path = this.PATH.EDIT_LESSON_TYPE;
              params = {
                name: content,
                type_id: this.table.editgroupId,
                sort: this.formValidate.sort
              };
            }
            this.$post(path, params).then(success => {
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
              this.getSubject()
            });
          } else {
            this.$Message.error("Fail!");
          }
        });
      }
    },

    created() {
      this.getSubject();
    }
  };
</script>
<style lang="scss">
  #typeManagement {
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
