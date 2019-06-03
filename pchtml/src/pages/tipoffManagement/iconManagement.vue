<template>
    <div id="bannerManagement">
       <div class="h1">icon管理</div>
      
       <Table class="zhijian-table account-table" stripe :columns="table.columns" :data="table.data"></Table>
        <!-- <div class="zhijian-pagination">
            <Page :total="table.total" :current="table.page" show-elevator @on-change="changePage" :pageSize="table.pagesize"></Page>
        </div> -->
        <!-- <div class="iconManagement_btn">
                <Button class="newbtn zhijian-new-btn" type="primary" @click="submitRe('module5')">提交</Button>
              </div> -->
    </div>
</template>
<script>
export default {
  name: "bannerManagement",
  data() {
    const validateImg = (rule, value, callback) => {
      if (this.h5Img == "") {
        callback(
          new Error(
            "请上传活动图片(大小不超过2M, 只支持png,jpg,jpeg,gif,bmp格式)"
          )
        );
      } else {
        callback();
      }
    };
    return {
      isShow: false, // 显示图片
      name: "",
      path: "",
      picurl: "",
      iconid: 0,
      table: {
        page: 1,
        pagesize: 10,
        total: 50,
        columns: [
          {
            title: "序号",
            key: "id",
            align: "center",
            width: 100
          },
          {
            title: "名称",
            key: "name",
            align: "center",
            // width: 200,
            render: (h, params) => {
              return h("input", {
                attrs: {
                  placeholder: "请输入",
                  value: params.row.name
                },
                style: {
                  background: "none",
                  outline: "none",
                  border: "0px",
                  textAlign: "center"
                },
                on: {
                  change: e => {
                    console.log(e.target.value);
                    this.name = e.target.value;
                  }
                }
              });
            }
          },
          {
            title: "图标",
            key: "pic",
            align: "center",
            // width: 400,
            render: (h, params) => {
              return h(
                "div",
                {
                  attrs: {
                    class: "button",
                    for: "inputFile"
                  },
                  on: {
                    click: e => {
                      this.iconid = params.row.id;
                      // console.log(e, "div");
                      // console.log(this.iconid,"inputFile"+params.row.id);
                      document.getElementById("inputFile"+params.row.id).click();
                    }
                  }
                },
                [
                  h("img", {
                    attrs: {
                      src:
                        this.iconid == params.row.id
                          ? this.picurl
                          : params.row.pic,
                      alt: "上传",
                      class: "iconwidth"
                    }
                  }),
                  h(
                    "span",
                    {
                      attrs: {
                        style:
                          params.row.pic == ""
                            ? "color:#ffc639"
                            : "display:none"
                      }
                    },
                    "上传"
                  ),
                  h("input", {
                    attrs: {
                      type: "file",
                      id: "inputFile"+params.row.id,
                      style: "display:none;"
                    },
                    on: {
                      change: e => {
                        console.log("pic", e);
                        let that = this;
                        let files = e.target.files || e.dataTransfer.files;
                        if (!files.length) return;
                        let type = e.target.files[0].type;
                        if (/^image/.test(type)) {
                          var reads = new FileReader();
                          reads.readAsDataURL(files[0]);
                          reads.onload = function() {
                            let fd = new FormData();
                            fd.append("data", this.result);
                            let config = {
                              headers: {
                                "Content-Type": "multipart/form-data"
                              }
                            };
                            that.$http
                              .post("/api/v1_0/uploadimage", {
                                type: "jpg",
                                data: this.result
                              })
                              .then(res => {
                                console.log(res);
                                that.picurl = res.data.url;
                              });
                          };
                        }
                      }
                    }
                  })
                ],
                this.iconid == params.row.id ? this.picurl : ""
              );
            }
          },
          {
            title: "跳转小程序路径",
            key: "jump_url",
            align: "center",
            // width:600,
            render: (h, params) => {
              return h("input", {
                attrs: {
                  placeholder: "请输入",
                  value: params.row.jump_url
                },
                style: {
                  background: "none",
                  outline: "none",
                  border: "0px",
                  textAlign: "center",
                  width: "100%"
                },
                on: {
                  change: e => {
                    console.log(e.target.value);
                    this.path = e.target.value;
                  }
                }
              });
            }
          },
          {
            title: "操作",
            align: "center",
            // width: 300,
            render: (h, params) => {
              return h("div", [
                h(
                  "button",
                  {
                    attrs: {
                      class: "newbtn zhijian-new-btn"
                    },
                    style: {
                      color: "#fff",
                      borderRadius: "10px",
                      width: "100px",
                      height: "40px",
                      lineHeight: "20px",
                      outline: "none",
                      border: "0px"
                    },
                    on: {
                      click: () => {
                        console.log(this.picurl);
                        console.log(this.name);

                        console.log(this.path);

                        let pic = this.picurl;
                        let path1 = this.path;
                        let that = this;
                        this.$http
                          .post(this.PATH.UPDATEICON, {
                            icon_id: params.row.id,
                            name: that.name || params.row.name,
                            pic: that.picurl || params.row.pic,
                            jump_url: that.path || params.row.jump_url
                          })
                          .then(success => {
                            console.log(success.data);
                            if (success.data.status == "200") {
                              this.$Modal.success({
                                width: 360,
                                content: success.data.msg,
                                onOk: () => {
                                  this.getdata();
                                }
                              });
                            }
                          });
                      }
                    }
                  },
                  "提交"
                )
              ]);
            }
          }
        ],

        data: []
      },
      h5Img: "",
      formValidate: {
        type: "new",
        row: {},
        sort: "",
        // link: "",
        status: "1"
      }
    };
  },
  created() {
    this.getdata();
  },
  methods: {
    //获取列表数据
    getdata() {
      this.$http.get(this.PATH.PCICONLIST).then(success => {
        console.log(success);
        if (success.status == 200) {
          if (success.data.errno == 0) {
            this.table.data = success.data.data;
          } else {
            this.$Modal.error({
              width: 360,
              content: success.data.errmsg
            });
          }
        } else {
          this.$Message.error("Fail!");
        }
      });
    }
  }
};
</script>
<style lang="scss">
#bannerManagement {
  height: 100%;
  padding: 20px;
  width: 100%;
  box-sizing: border-box;
  -webkit-box-sizing: border-box;
  .h1 {
    font-size: 22px;
    color: #808080;
  }
  .iconwidth {
    width: 35px;
    height: 35px;
  }
  .iconheight {
    width: 0;
    height: 0;
  }
  .zhijian-table {
    margin-top: 20px;
  }
  .iconManagement_btn {
    margin-top: 20px;
  }
}
</style>
