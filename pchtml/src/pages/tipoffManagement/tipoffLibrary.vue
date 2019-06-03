<template>
  <div id="tipoffLibrary">
    <div class="h1">爆料库
      <div class="search">
        <Input
          v-model="words"
          search
          enter-button="搜索"
          @on-search="searchTipoff"
          placeholder="请输入搜索关键字"
        />
      </div>
    </div>

    <div class="header">
      <DatePicker
        v-model="startDate"
        type="date"
        placeholder="开始日期"
        style="width: 120px;"
        @on-change="getStart"
      ></DatePicker>至
      <DatePicker
        type="date"
        v-model="endDate"
        placeholder="结束日期"
        style="width:120px;"
        @on-change="getEnd"
      ></DatePicker>
      <Select
        v-model="arcSource"
        style="width:100px;margin-right:270px"
        placeholder="全部来源"
        @on-change="getCate"
      >
        <Option value>全部来源</Option>
        <Option v-for="item in articleSource" :value="item" :key="item">{{ item }}</Option>
      </Select>
      <Button class="newbtn zhijian-new-btn" type="primary" @click="showLinkModal()">新增</Button>
      <Button class="newbtn1 zhijian-new-btn" type="primary" @click="uploadStatus1">批量上线</Button>
      <Button class="newbtn2 zhijian-new-btn" type="primary" @click="delectArcs">批量删除</Button>
    </div>
    <Table
      class="zhijian-table account-table"
      stripe
      :columns="table.columns"
      :data="table.data"
      ref="selection"
      @on-selection-change="onArc"
      @on-select-all="onlineArc"
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
    <!-- 设置头图编辑框 -->
    <Modal :mask-closable="false" v-model="editPicModal" width="535" class-name="ma-upload-modal">
      <div class="edit-modal-body">
        <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80">
          <FormItem label="上传图片" prop="uploadimg">
            <div class="h5ImgBox" v-if="isShow">
              <img :src="h5Img" style="width:98px;height:98px;">
            </div>
            <div>
              <label for="inputFile" class="button">
                <span class="upload__select">点击上传图片</span>
                <input
                  type="file"
                  id="inputFile"
                  accept="image/gif, image/jpeg, image/png, image/jpg"
                  style="display:none"
                  @change="onUpload"
                >
              </label>
            </div>
          </FormItem>
        </Form>
      </div>
      <div class="zhijian-btn-box">
        <div class="zhijian-btn-confirm" @click="submitForm('formValidate')">确定</div>
      </div>
    </Modal>
    <!-- 设置上线编辑框 -->
    <Modal :mask-closable="false" v-model="uploadModal" width="535" class-name="ma-upload-modal">
      <div class="edit-modal-body">
        <div class="title">请选择需要上线的类型</div>
        <Checkbox-group
          v-model="checkedGroup"
          v-for="item in groups"
          :key="item.groups"
          @on-change="checkMoreGroupChange"
        >
          <Checkbox :label="item.group_id">{{item.group_name}}</Checkbox>
        </Checkbox-group>
      </div>
      <div class="zhijian-btn-box">
        <div class="zhijian-btn-confirm" @click="editcategory">确定</div>
      </div>
    </Modal>
    <!--单篇文章新增抓取  -->
    <Modal :mask-closable="false" v-model="addLinkModal" width="535" class-name="ma-edit-modal">
      <div class="edit-modal-body hint">
        <Icon type="android-close" @click="editModal=false"></Icon>
        <Form ref="formValidate1" :model="formValidate1" :rules="ruleValidate1" :label-width="100">
          <FormItem label="文章链接" prop="link">
            <Input v-model="formValidate1.link" type="text" placeholder="请输入文章链接"></Input>
          </FormItem>
          <FormItem label>
            <p style="color:#ccc;">*请使用移动端进入公众号文章复制链接</p>
            <!-- https://mp.weixin.qq.com/s/O4nFwUocih37UHErbnaq4g -->
          </FormItem>
        </Form>
      </div>
      <div class="zhijian-btn-box">
        <Button
          class="newbtn zhijian-new-btn"
          type="primary"
          @click="submitLinkForm('formValidate1')"
          v-if="isHide"
        >确定</Button>
        <Col class="demo-spin-col" span="8" v-show="isLoding">
          <Spin fix>加载中...</Spin>
        </Col>
        <!-- <div class="zhijian-btn-confirm" @click="submitLinkForm('formValidate1')" :disabled="isDisable">确定</div> -->
      </div>
    </Modal>
    <!-- 显示文章详情 -->
    <Modal v-model="detailModal" title="Common Modal dialog box title" width="735">
      <div class="detail">
        <h1>{{art_detail.title}}</h1>
        <div class="come-from">
          <span>转载：{{art_detail.author}}</span>
          <span>{{art_detail.wechat_art_date}}</span>
        </div>
        <div v-for="(item, index) in art_detail.content" :key="index">
          <p class="cont-text" v-if="item.text">{{item.text}}</p>
          <img class="cont-img" mode="aspectFit" v-else :src="item.img" alt>
        </div>
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
          new Error("请上传文章头图(大小不超过2M, 只支持jpg,jpeg,gif,bmp格式)")
        );
      } else {
        callback();
      }
    };
    return {
      is_search: "",
      words: "", //关键字
      startDate: "", //开始时间
      endDate: "", //结束时间
      arcSource: "", //来源
      editPicModal: false,
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
      isLoding: false,
      isHide: true,
      onlineid: 0,
      detailModal: false,
      art_detail: {},
      checkedArc: [], //批量处理
      table: {
        page: 1,
        pagesize: 20,
        total: 50,
        columns: [
          {
            type: "selection",
            title: "全选",
            width: 60,
            align: "center"
          },
          {
            title: "内容",
            key: "content",
            width: 500,
            render: (h, params) => {
              return h(
                "div",
                {
                  style: {
                    display: "flex",
                    alignItems: "center",
                    height: "120px"
                  },
                  on: {
                    click: () => {
                      console.log(params);
                      this.detailModal = true;
                      this.onlineid = params.row.article_id;
                      this.getDetail();
                    }
                  }
                },
                [
                  h(
                    "div",
                    {
                      style: {
                        width: "160px",
                        height: "90px",
                        overflow: "hidden",
                        marginRight: "20px",
                        position: "relative"
                      }
                    },
                    [
                      h("img", {
                        attrs: {
                          src: params.row.min_pic
                        },
                        style: {
                          width: "160px"
                        }
                      })
                    ]
                  ),
                  h(
                    "div",
                    {
                      style: {}
                    },
                    [
                      h(
                        "p",
                        {
                          style: {
                            fontSize: "18px",
                            color: "#999",
                            width: "300px",
                            overflow: "hidden",
                            textOverflow: "ellipsis",
                            display: "-webkit-box",
                            webkitLineClamp: 2,
                            webkitBoxOrient: "vertical"
                          }
                        },
                        params.row.title
                      ),
                      h(
                        "p",
                        {
                          style: {
                            fontSize: "18px",
                            color: "#999",
                            width: "300px"
                          }
                        },
                        [
                          h("span", "转载："),
                          h(
                            "span",
                            {
                              style: {
                                color: "blue"
                              }
                            },
                            params.row.author
                          )
                        ]
                      )
                    ]
                  )
                ]
              );
            }
          },
          {
            title: "文章发布时间",
            key: "wechat_art_date",
            // width: 200,
            align: "center",
            render: (h, params) => {
              return h(
                "div",
                this.formatMoment(params.row.wechat_art_date, "MM月DD日")
              );
            }
          },
          {
            title: "操作",
            align: "center",
            // width: 400,
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
                        this.onUploadPic(
                          params.row.min_pic,
                          params.row.article_id
                        );
                      }
                    }
                  },
                  "设置头图"
                ),
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
                        this.uploadStatus(params.row.article_id);
                      }
                    }
                  },
                  "上线"
                ),
                h(
                  "i-button",
                  {
                    on: {
                      click: () => {
                        this.$Modal.warning({
                          content: "确定删除该爆料吗?",
                          onOk: () => {
                            this.deleteTipoff(params.row.article_id);
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
          { required: true, message: "请输入要抓取的文章链接", trigger: "blur" }
        ]
      }
    };
  },
  methods: {
    //渲染爆料库列表数据
    getData() {
      console.log("刷新");
      this.$http
        .post(this.PATH.ARTICLES, {
          page: this.table.page,
          pagesize: this.table.pagesize,
          is_show: 0
        })
        .then(res => {
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
    //日期格式化（用的moment插件）
    formatMoment(value, formatString) {
      formatString = formatString || "YYYY-MM-DD HH:mm:ss";
      return moment(value).format(formatString);
    },
    //获取选择的开始时间
    getStart(value) {
      this.startDate = value;
    },
    //获取结束时间
    getEnd(value) {
      this.endDate = value;
    },
    //获取来源
    getCate(value) {
      this.arcSource = value;
    },
    //搜索功能
    searchTipoff() {
      this.is_search = true;
      this.$http
        .post(this.PATH.ARTICLESSearch, {
          page: this.table.page,
          words: this.words,
          web_name: this.arcSource,
          start_time: this.startDate,
          end_time: this.endDate,
          is_show: 0
        })
        .then(res => {
          console.log(res);
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
    //单篇抓取文章
    showLinkModal() {
      this.addLinkModal = true;
    },
    submitLinkForm(name) {
      console.log("确定");
      this.isHide = false;
      this.isLoding = true;

      this.$refs[name].validate(valid => {
        if (valid) {
          // console.log(this.formValidate1.link);
          let path = "";
          let params = new Object();
          path = this.PATH.WECHATURL;
          params = {
            url: this.formValidate1.link
          };
          this.$http.post(path, params).then(success => {
            console.log(success);
            if (success.status == 200) {
              this.isHide = true;

              this.isLoding = false;
              this.$Modal.error({
                width: 360,
                content: success.data.errmsg
              });
              this.addLinkModal = false;
              this.formValidate1.link = "";
              this.getData();
            } else {
              this.$Modal.error({
                width: 360,
                content: success.data.errmsg
              });
            }
          });
        } else {
          this.$Message.error("Fail!");
        }
      });
    },
    //根据id删除某条爆料信息
    deleteTipoff(articleid) {
      let list = [];
      list.push(articleid);
      this.$http
        .post(this.PATH.DELARTICLE, {
          article_id_list: list
        })
        .then(res => {
          console.log(res, "del");
          if (res.data.errno == 0) {
            console.log("jinru");
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
            .post(this.PATH.DELARTICLE, {
              article_id_list: this.checkedArc
            })
            .then(res => {
              console.log(res.data.errmsg, "del");
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
    //设置头图
    onUploadPic(mainurl, articleid) {
      console.log("上传头图");
      this.editPicModal = true; //显示模态框
      this.h5Img = mainurl;
      this.articleid_img = articleid;
      this.isShow = true;
    },
    //修改后台头图
    submitForm(name) {
      console.log("hhh");
      this.$refs[name].validate(valid => {
        if (valid) {
          let type = this.formValidate.type;
          let path = "";
          let params = new Object();
          path = this.PATH.MINPIC;
          params = {
            article_id: this.articleid_img,
            img: this.formValidate.main_img
          };
          this.$http.post(path, params).then(success => {
            this.$Message.success(success.data.errmsg);
            this.editPicModal = false;
            this.getData();
          });
        } else {
          this.$Message.error("Fail!");
        }
      });
    },
    //上传图片
    onUpload(e) {
      console.log("qqq");
      let files = e.target.files || e.dataTransfer.files;
      console.log("files", files);
      if (!files.length) return;
      let type = e.target.files[0].type;
      let typeArr = ["png", "jpg", "jpeg", "gif", "bmp"];
      if (
        type == "" ||
        typeArr.indexOf(type.split("/")[1]) < 0 ||
        e.target.files[0].size > 2 * 1024 * 1024
      ) {
        this.h5Img = "";
        this.$refs.formValidate.validateField("qrcard");
        return;
      }
      var reads = new FileReader();
      reads.readAsDataURL(files[0]); //转为base64
      let that = this;
      reads.onload = function(e) {
        var fd = new FormData();
        fd.append("bs4", this.result);
        let config = {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        };
        let path = that.PATH.UPLOADIMAGE;
        that.$http
          .post(path, {
            type: type,
            data: this.result
          })
          .then(
            success => {
              if (success.data.status == "0") {
                that.isShow = true;
                that.h5Img = success.data.url;
                that.formValidate.main_img = success.data.url;
                that.$refs.formValidate.validateField("uploadimg");
              } else {
                that.$Modal.error({
                  title: "提示",
                  content: success.data.errmsg
                });
              }
            },
            error => {
              this.$Modal.error({
                title: "提示",
                content: "上传失败，请重试"
              });
            }
          );
      };
    },
    //获取文章来源
    getArticleSourse() {
      this.$http
        .post(this.PATH.ARTICLESOURCE, {
          is_show: 0
        })
        .then(res => {
          if (res.data.errno == 0) {
            this.articleSource = res.data.data;
          } else {
            this.$Modal.error({
              width: 360,
              content: res.data.errmsg
            });
          }
        });
    },
    //获取上线类型
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
    //设置上线
    uploadStatus(articleid) {
      this.uploadModal = true;
      this.checkedArc.push(articleid);
      this.getGroups();
    },
    //设置上线
    uploadStatus1() {
      this.uploadModal = true;
      this.getGroups();
    },
    // 全选拿到选中的文章id
    onlineArc(selection) {
      this.checkedArc = [];
      selection.forEach(v => {
        this.checkedArc.push(v.article_id);
      });
      console.log(this.checkedArc, "全选");
    },
    // onselectchange(selection){
    //   console.log(selection,'123');
    // },
    // 多选拿到选中的文章id
    onArc(selection) {
      this.checkedArc = [];
      selection.forEach(v => {
        this.checkedArc.push(v.article_id);
      });
      console.log(selection);
      console.log(this.checkedArc, "多选");
    },
    //多选选择的上线类型
    checkMoreGroupChange(data) {
      this.checkedGroup = data;
    },
    //修改文章上线
    editcategory() {
      let arr = this.checkedGroup;
      this.$http
        .post(this.PATH.ONLINE, {
          article_id_list: this.checkedArc,
          group_id_list: arr
        })
        .then(res => {
          if (res.data.errno == 0) {
            console.log(res.data, "上线");
            this.$Modal.error({
              width: 360,
              content: res.data.errmsg
            });
            this.checkedArc = []; //清空多选文章id
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
    // 获取文章详情
    getDetail() {
      this.art_detail = {};
      this.$http
        .post(this.PATH.ARTICLEDETAILS, {
          article_id: this.onlineid
        })
        .then(res => {
          console.log(res);
          if (res.data.errno == 0) {
            this.art_detail = res.data.data;
          } else {
            this.$Modal.error({
              width: 360,
              content: res.data.errmsg
            });
          }
        });
    }
  },
  //进入页面就渲染列表数据
  created() {
    this.getData();
    this.getGroups();
    this.getArticleSourse();
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
