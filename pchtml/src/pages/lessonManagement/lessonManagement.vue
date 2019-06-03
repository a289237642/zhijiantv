<template>
    <div id="tipoffList">
        <h1>免费领取课程列表</h1>
        <!-- <Input v-model="value" class="search" search enter-button="搜索" @on-search="search" @on-blur="changePages" placeholder="请输入搜索关键字"/> -->
        <!-- <Button class="newbtn1 zhijian-new-btn" type="primary" @click="showEditModal('new')">新增</Button> -->

        <Button class="newbtn zhijian-new-btn" type="primary" @click="downLesson">批量下架</Button>
        <!-- <Button class="newbtn zhijian-new-btn" type="primary" @click="upLesson" v-else>批量上架</Button> -->
          <Tabs :value="name0" @on-click="handTabClick"> 
            <TabPane label="线上全部课程" name="name0">
                 <Table class="tip-table" border :columns="columns2" :data="data2" ref="selection"  @on-selection-change="downlesson" @on-select-all="downlinelesson"></Table>
                <div class="zhijian-pagination">
                    <Page :total="table.totalAll" :current="table.page" show-elevator @on-change="changePageAll" :pageSize="table.pagesize"></Page>
                </div>
            </TabPane>
            <TabPane :label="item.name" :name="item.type_id + ''"  v-for="item in uptypelist" :value="item.type_id" :key="item.type_id" >
              
                <Table class="tip-table" border :columns="columns3" :data="data3" ref="selection"  @on-selection-change="downlesson" @on-select-all="downlinelesson"></Table>
                <div class="zhijian-pagination">
                    <Page :total="table.totalAll1" :current="table.page" show-elevator @on-change="changePageAll1" :pageSize="table.pagesize"></Page>
                </div>
                
            </TabPane>
        </Tabs>

        <!-- 是否上、下架 -->
        <Modal v-model="updownModal" title="Common Modal dialog box title" >
          <div>
            <!-- 下架 -->
            <p style="text-align:center;margin:10px 0;">是否确定下架该课程？</p>
            <div class="zhijian-btn-box" style="margin-top:20px">
                <div class="zhijian-btn-confirm" @click="downOk">确定</div>
            </div>
          </div>
        </Modal>
  
        <!-- 移动 -->
        <Modal v-model="moveModal" title="Common Modal dialog box title" class-name="ma-edit-modal">
           <div class="edit-modal-body">
                <div class="title" style="font-size:24px;color: var(--base);text-align:center">移动</div>
                   <RadioGroup v-model="animal" style="margin:20px 80px;">
                      <Radio label="1">上移</Radio>
                      <Radio label="2">下移</Radio>
                      <Radio label="3">移至顶部</Radio>
                      <Radio label="4">移至底部</Radio>
                  </RadioGroup>
            </div>
            <div class="zhijian-btn-box">
                <div class="zhijian-btn-confirm" @click="moveOk">确定</div>
            </div>
         
        </Modal>
        <!-- 删除 -->
         <Modal v-model="delemodal" title="Common Modal dialog box title">
            <p class="modelp">请确认是否删除改课程</p>
            <div class="zhijian-btn-box">
                <div class="zhijian-btn-confirm" @click="deleteOk">确定</div>
            </div>
        </Modal>
       
    </div>
</template>
<script>
export default {
  name: "tipoffList",
  data() {
    return {
      editModal: false, //展示新增编辑弹框
      moveModal: false, //移动弹窗
      animal: "1", //移动方式
      updownModal: false, //上下架
      confirm: "请确认是否上架该课程",
      delemodal: false, //删除课程
      // is_search: false,
      startDate: "",
      h5Img: "",
      h5Img1: "",
      endDate: "",
      endtime: "",
      name0: "name0",
      paramses: {},
      is_show: 1,
      isShow: true,
      lessonid: 1,
      audioid:1,
      deatillesson: {},
      detailModal: false,
      uptypelist: [],
      uptype: "1",
      checkedGroup: [],
      audiopath: "",
      addaudioModal: false,
      moveaudioModal: false,
      author: "",
      audioModal: false,
      deleaudiomodal: false,
      checkedLesson: [], //批量上架、下架
      checkedaudio: [],
      type_id:"name0",
      table: {
        total: 10,
        totalAll: 10,
        totalAll1:10,
        totalSearch: 10,
        page: 1,
        pagesize: 10,
        is_show: 1
      },
      formValidate: {
        type: "new",
        cost_type: "1"
      },
      ruleValidate: {
        title: [{ required: true, message: "标题", trigger: "blur" }],
        cost_type: [
          { required: true, message: "请选择支付类型", trigger: "blur" }
        ]
      },
      columns2: [
        {
          type: "selection",
          title: "全选",
          width: 60,
          align: "center",
          key: "id"
        },
        {
          title: "序号",
          key: "location",
          // width: 100
        },
        {
          title: "ID",
          key: "lesson_id",
          // width: 100
        },
        {
          title: "课程名称",
          key: "title",
          // width: 200,
          render: (h, params) => {
            return h(
              "div",
              {
                style: {
                  display: "flex",
                  alignItems: "center"
                },
                on: {
                  click: () => {
                    console.log(params);
                    this.editModal = true;
                    // this.onlineid = params.row.article_id;
                    this.showEditModal("edit", params.row);
                  }
                }
              },
              params.row.title
            );
          }
        },
        {
          title: "音频数",
          key: "audio_num",
          // width: 90,
          render: (h, params) => {
            return h(
              "div",
              {
                style: {},
                on: {
                  click: () => {
                    this.$router.push({
                      name: "lessonAudio",
                      params: { lessonid: params.row.id }
                    });
                  }
                }
              },
              params.row.audio_num
            );
          }
        },
        {
          title: "创建人",
          key: "author",
          // width: 100
        },
        {
          title: "领取人数",
          key: "buy_num",
          // width: 90
        },
        {
          title: "到期时间",
          key: "end_time",
          // width: 150
        },
         {
          title: "生成次数(邀友助力)",
          key: "help_bron_qr_num",
          // width: 90
        },
         {
          title: "生成次数(邀友听课)",
          key: "listen_bron_qr_num",
          // width: 90
        },
        {
          title: "进入总次数",
          key: "scan_qr_num",
          // width: 90
        },
        {
          title: "操作",
          key: "action",
          // width: 450,
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "normal",
                    class: "btn"
                  },
                  style: {
                    background: params.row.is_show == "1" ? "white" : "black",
                    border:
                      params.row.is_show == "1" ? "1px solid black" : "none",
                    color: params.row.is_show == "1" ? "black" : "white",
                    marginRight: "5px"
                  },
                  on: {
                    click: () => {
                      this.paramses = params;
                      this.updownModal = true;
                      this.is_show = params.row.is_show;
                      this.getuplist();
                      console.log(params);
                    }
                  }
                },
                params.row.is_show == "1" ? "下架" : "上架"
              ),

              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "normal",
                    class: "btn"
                  },
                  style: {
                    background: "black",
                    border: "none",
                    marginRight: "5px",
                    display: params.row.is_show == "1" ? "none" : ""
                  },
                  on: {
                    click: () => {
                      console.log("delete");
                      this.delemodal = true;
                      this.paramses = params;
                    }
                  }
                },
                "删除"
              )
            ]);
          }
        }
      ],
      columns3: [
        {
          type: "selection",
          title: "全选",
          width: 60,
          align: "center",
          key: "id"
        },
        {
          title: "序号",
          key: "sort_num",
          // width: 100
        },
        {
          title: "ID",
          key: "lesson_id",
          // width: 100
        },
        {
          title: "课程名称",
          key: "title",
          // width: 200,
          render: (h, params) => {
            return h(
              "div",
              {
                style: {
                  display: "flex",
                  alignItems: "center"
                },
                on: {
                  click: () => {
                    console.log(params);
                    this.editModal = true;
                    this.showEditModal("edit", params.row);
                  }
                }
              },
              params.row.title
            );
          }
        },
        {
          title: "音频数",
          key: "audio_num",
          // width: 90,
          render: (h, params) => {
            return h(
              "div",
              {
                style: {},
                on: {
                  click: () => {
                    this.$router.push({
                      name: "lessonAudio",
                      params: { lessonid: params.row.id }
                    });
                  }
                }
              },
              params.row.audio_num
            );
          }
        },
        {
          title: "创建人",
          key: "author",
          // width: 100
        },
        {
          title: "领取人数",
          key: "buy_num",
          // width: 90
        },
        {
          title: "到期时间",
          key: "end_time",
          // width: 150
        },
          {
          title: "生成次数(邀友助力)",
          key: "help_bron_qr_num",
          // width: 90
        },
         {
          title: "生成次数(邀友听课)",
          key: "listen_bron_qr_num",
          // width: 90
        },
        {
          title: "进入总次数",
          key: "scan_qr_num",
          // width: 90
        },
        {
          title: "操作",
          key: "action",
          // width: 450,
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "normal",
                    class: "btn"
                  },
                  style: {
                    background: params.row.is_show == "1" ? "white" : "black",
                    border:
                      params.row.is_show == "1" ? "1px solid black" : "none",
                    color: params.row.is_show == "1" ? "black" : "white",
                    marginRight: "5px"
                  },
                  on: {
                    click: () => {
                      this.paramses = params;
                      this.updownModal = true;
                      this.is_show = params.row.is_show;
                      this.getuplist();
                      // console.log(params,'222');
                    }
                  }
                },
                params.row.is_show == "1" ? "下架" : "上架"
              ),

              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "normal",
                    class: "btn"
                  },
                  style: {
                    background: "black",
                    border: "none",
                    marginRight: "5px",
                    display: params.row.is_show == "1" ? "none" : ""
                  },
                  on: {
                    click: () => {
                      // console.log("delete");
                      this.delemodal = true;
                      this.paramses = params;
                    }
                  }
                },
                "删除"
              ),
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "normal",
                    class: "btn"
                  },
                  style: {
                    background: "black",
                    border: "none",
                    marginRight: "30px",
                    display: params.row.is_show == "0" ? "none" : ""
                  },
                  on: {
                    click: () => {
                      this.paramses = params;
                      this.moveModal = true;
                    }
                  }
                },
                "移动"
              )
            ]);
          }
        }
      ],
      data2: [],
      data3: []
    };
  },
  methods: {
    // 全部上架课程
    getLessonsAll() {
      this.$http
        .post(this.PATH.PCLESSONS, {
          page: this.table.page,
          pagesize: this.table.pagesize,
          is_show: 1 ,//0是已下架 1已上架
        })
        .then(res => {
          console.log(res);
          if (res.status == 200) {
            if (res.data.errno == 0) {
              this.data2 = res.data.data;
              this.table.totalAll = res.data.count;
            } else {
              this.$Message.success(res.data.errmsg);
            }
          } else {
            this.$Message.error("Fail!");
          }
        });
    },
    // 分类上架课程
      getTypeLessons(typeid) {
      this.$http
        .post(this.PATH.PCLESSSONLIST, {
          page: this.table.page,
          pagesize: this.table.pagesize,
          type_id: typeid ,//0是已下架 1已上架

        })
        .then(res => {
          console.log(res);
          if (res.status == 200) {
            if (res.data.errno == 0) {
              this.data3 = res.data.data;
              this.table.totalAll1 = res.data.count;
              console.log(this.table.totalAll1);
            } else {
              this.$Message.success(res.data.errmsg);
            }
          } else {
            this.$Message.error("Fail!");
          }
        });
    },
    // 下架课程
    getdownlesson() {
      this.$http.get(this.PATH.GETLESSONDOWN).then(res => {
        console.log(res);
      });
    },
    // 课程类型
    getuplist() {
      this.$http
        .post(this.PATH.PCGETLESSONTYPE, {
          page: 1,
          pagesize: 50
        })
        .then(res => {
          console.log(res);
          if (res.status == 200) {
            if (res.data.errno == 0) {
              this.uptypelist = res.data.data;
            } else {
              this.$Modal.error({
                width: 360,
                content: res.data.errmsg
              });
            }
          } else {
            this.$Message.error("Fail!");
          }
        });
    },
    // 课程音频
    getLessonsAudio() {
      this.$http
        .post(this.PATH.LESSONAUDIOLIST, {
          page: this.table.page,
          pagesize: this.table.pagesize,
          lesson_id: this.lessonid //课程id
        })
        .then(res => {
          console.log(res);
          if (res.status == 200) {
            if (res.data.errno == 0) {
              this.data3 = res.data.data;
              this.table.totalAll = res.data.count;
            } else {
              this.$Modal.error({
                width: 360,
                content: res.data.errmsg
              });
            }
          } else {
            this.$Message.error("Fail!");
          }
        });
    },
    // 完成
    audioOk() {
      this.audioModal = false;
      this.table.page = 1;
      this.getLessonsAll();
    },
    //切换tab栏
    handTabClick(typeid) {
      this.name0 = typeid;
      console.log(typeid);
      this.is_search = false;
      this.type_id = typeid;
      if (typeid == "name0") {
        this.is_show = 1;
        this.getLessonsAll();
      } else {
        this.is_show = 0;
        this.getTypeLessons(typeid);
      }
    },
    //展示弹框
    showEditModal(type, row) {
      this.formValidate.type = type;
      //对整个表单进行重置，将所有字段值重置为空并移除校验结果
      // this.$refs.formValidate.resetFields();
      if (type == "new") {

      } else {
        this.$http
          .post(this.PATH.PCLESSONDETAIL, {
            lesson_id: row.id
          })
          .then(success => {
            if (success.status == 200) {
              if (success.data.errno == 0) {
                this.deatillesson = success.data.data;
                this.formValidate.title = this.deatillesson.title;
                this.formValidate.subtitle = this.deatillesson.subtitle;
                this.h5Img = this.deatillesson.min_pic;
                this.formValidate.count = this.deatillesson.count;
                this.h5Img1 = this.deatillesson.summary;
                this.endDate = this.deatillesson.end_time;
                this.cost_type = this.deatillesson.cost_type;
                this.formValidate.present_num = this.deatillesson.present_num;
                this.formValidate.base_num = this.deatillesson.base_num;
                this.formValidate.price = this.deatillesson.price;
                this.lessonid = row.id;
                this.author = row.author;
              } else {
                this.$Modal.success({
                  title: "提示",
                  content: success.data.errmsg
                });
              }
            } else {
              this.$Message.error("Fail!");
            }
          });
      }
      this.editModal = true;
      // this.audioModal = true;
    },
    //上传头图片
    onUpload(e) {
      let files = e.target.files || e.dataTransfer.files;
      if (!files.length) return;
      let type = e.target.files[0].type;
      let typeArr = ["png", "jpg", "jpeg", "gif", "bmp"];

      var reads = new FileReader();
      reads.readAsDataURL(files[0]);
      let that = this;
      reads.onload = function(e) {
        var fd = new FormData();
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
          .then(
            success => {
              if (success.data.status == "0") {
                that.isShow = true;
                that.h5Img = success.data.url;
              } else {
                that.$Modal.error({
                  title: "提示",
                  content: success.data.msg
                });
              }
            },
            error => {
              this.$Modal.error({
                title: "提示",
                content: success.data.msg
              });
            }
          );
      };
    },
    //上传课程图片
    onUpload1(e) {
      let files = e.target.files || e.dataTransfer.files;
      if (!files.length) return;
      let type = e.target.files[0].type;
      let typeArr = ["png", "jpg", "jpeg", "gif", "bmp"];

      var reads = new FileReader();
      reads.readAsDataURL(files[0]);
      let that = this;
      reads.onload = function(e) {
        var fd = new FormData();
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
          .then(
            success => {
              if (success.data.status == "0") {
                that.isShow = true;
                that.h5Img1 = success.data.url;
              } else {
                that.$Modal.error({
                  title: "提示",
                  content: success.data.msg
                });
              }
            },
            error => {
              this.$Modal.error({
                title: "提示",
                content: success.data.msg
              });
            }
          );
      };
    },
    // 上传音频
    onUpload3(e) {
      let that = this;
      let files = e.target.files || e.dataTransfer.files;
      if (!files.length) return;
      var fd = new FormData();
      fd.append("file", e.target.files[0]);
      let config = {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      };
      console.log(fd.get("file"));
      this.$Spin.show({
        render: h => {
          return h("div", [
            h("Icon", {
              class: "demo-spin-icon-load",
              props: {
                type: "ios-loading",
                // size: 18
              }
            }),
            h("div", "上传中...")
          ]);
        }
      });
      that.$http.post("/api/v1_0/upload_audio", fd).then(
        success => {
          console.log(success);
          if (success.data.errno == "0") {
            that.isShow = true;
            that.audiopath = success.data.mp3_url;
            that.$Spin.hide();
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
            content: success.data.msg
          });
        }
      );
      this.getLessonsAudio();
    },
   

    // sessionStorage.getItem('username'),
    submitForm(name) {
      // console.log(111);
      this.$refs[name].validate(valid => {
        if (valid) {
          let type = this.formValidate.type;
          let path = "";
          let params = new Object();
          if (type == "new") {
            //新增
            path = this.PATH.ADDLESSON;
            params = {
              title: this.formValidate.title,
              subtitle: this.formValidate.subtitle,
              author: sessionStorage.getItem("username"),
              min_pic: this.h5Img,
              count: this.formValidate.count,
              summary: this.h5Img1,
              count: this.formValidate.count,
              end_time: this.endDate,
              cost_type: 1,
              present_num: this.formValidate.present_num,
              base_num: this.formValidate.base_num,
              price: this.formValidate.price
            };
          } else {
            path = this.PATH.EDITLESSON;
            params = {
              lesson_id: this.lessonid,
              title: this.formValidate.title,
              subtitle: this.formValidate.subtitle,
              author: this.author,
              min_pic: this.h5Img,
              count: this.formValidate.count,
              summary: this.h5Img1,
              count: this.formValidate.count,
              end_time: this.endDate,
              cost_type: 1,
              present_num: this.formValidate.present_num,
              base_num: this.formValidate.base_num,
              price: this.formValidate.price
            };
          }
          this.$http.post(path, params).then(success => {
            console.log(success.data);
            if (success.data.errno == 0) {
              this.editModal = false;
              this.audioModal = true;
              this.data3 = [];
              this.lessonid = success.data.lesson_id;
              // this.$Modal.success({
              //   title: "提示",
              //   content: success.data.errmsg,
              //   onOk: () => {
              //     this.editModal = false;
              //     this.formValidate.title='';
              //     this.formValidate.subtitle='';
              //     this.h5Img='';
              //     this.formValidate.count='';
              //     this.h5Img1='';
              //     this.endDate='';
              //     this.formValidate.present_num='';
              //     this.formValidate.base_num='';
              //     this.formValidate.price='';
              //     this.lessonid = success.data.lesson_id;
              //   }
              // });
            } else {
              this.$Modal.success({
                title: "提示",
                content: success.data.errmsg,
                onOk: () => {
                  // this.editModal = false;
                }
              });
            }
            this.table.page = 1;
            this.getLessonsAll();
          });
        } else {
          this.$Message.error("Fail!");
        }
      });
    },
    // 全选拿到选中的课程id
    downlinelesson(selection) {
      this.checkedLesson = [];
      selection.forEach(v => {
        this.checkedLesson.push(v.id);
      });
      console.log(this.checkedLesson, "全选");
    },
    // 多选拿到选中的课程id
    downlesson(selection) {
      this.checkedLesson = [];
      selection.forEach(v => {
        this.checkedLesson.push(v.id);
      });
      console.log(this.checkedLesson, "多选");
    },
    //多选选择的上线类型
    checkMoreGroupChange(data) {
      this.checkedGroup = data;
    },
    //批量上架
    upLesson() {
      this.updownModal = true;
      this.getuplist();
    },
    //批量下架
    downLesson() {
      // let list = [];
      this.updownModal = true;
      console.log(this.type_id);
      if(this.type_id=="name0"){
        this.$http
        .post(this.PATH.DOWNLESSON, {
          lesson_id_list: this.checkedLesson
        })
        .then(res => {
          console.log(res);
          if (res.data.errno == 0) {
            this.$Message.success(res.data.errmsg);
            this.getLessonsAll();
          }
        });
      }else{
         this.$http
        .post(this.PATH.DOWNLESSON, {
          lesson_id_list: this.checkedLesson,
          type_id:this.type_id
        })
        .then(res => {
          console.log(res);
          if (res.data.errno == 0) {
            this.$Message.success(res.data.errmsg);
            this.getTypeLessons(this.type_id);
          }
        });
      }
      this.updownModal = false; //隐藏弹框
    },
    //上架(批量)
    upok() {
      let list = [];
      console.log(this.checkedLesson);
      if(this.checkedLesson.length==0){
         list.push(this.paramses.row.id);
      }else{
          list = this.checkedLesson;
      }
      // list.push(this.paramses.row.id);
      this.$http
        .post(this.PATH.UPLOADLESSONS, {
          lesson_id_list: list,
          end_time: this.endDate,
          type_id_list: this.checkedGroup
        })
        .then(res => {
          console.log(res);
          if (res.data.errno == 0) {
            this.$Message.success(res.data.errmsg);
            this.checkedLesson=[];
            this.getLessonsAll();
          }
        });
      this.updownModal = false; //隐藏弹框
    },
    //下架
    downOk() {
      let list = [];
      console.log(this.paramses,'111');
      list.push(this.paramses.row.id);
      let typeid = this.type_id;
      if(typeid=='name0'){
         this.$http
        .post(this.PATH.DOWNLESSON, {
          lesson_id_list: list
        })
        .then(res => {
          console.log(res);
          if (res.data.errno == 0) {
            this.$Message.success(res.data.errmsg);
            this.getLessonsAll();
          }
        });
      }else{
        this.$http
        .post(this.PATH.DOWNLESSON, {
          lesson_id_list: list,
          type_id: this.type_id
        })
        .then(res => {
          console.log(res);
          if (res.data.errno == 0) {
            this.$Message.success(res.data.errmsg);
            this.getTypeLessons(this.type_id);
          }
        });
      }
      
      this.updownModal = false; //隐藏弹框
    },
    deleteOk() {
      console.log(111);
      let list = [];
      list.push(this.paramses.row.id);
      this.$http
        .post(this.PATH.DELETELESSON, {
          lesson_id_list: list
        })
        .then(res => {
          console.log(res);
          if (res.data.errno == 0) {
           this.$Message.success(res.data.errmsg);
            this.getLessonsAll();
          } else {
            this.$Message.success(res.data.errmsg);
          }
        });
      this.delemodal = false;
    },
    changePageAll(page) {
      this.table.page = page;
      this.getLessonsAll();
    },
     changePageAll1(page) {
      this.table.page = page;
       this.getTypeLessons(this.type_id);
    },
    //确定保存移动设置
    moveOk() {
      this.$http
        .post(this.PATH.LESSONMOVE, {
          lesson_id: this.paramses.row.id,
          sort_num: this.paramses.row.sort_num,
          move: this.animal,
          type_id:this.type_id
        })
        .then(res => {
          console.log(res);
          if (res.status == 200) {
           this.$Message.success(res.data.errmsg);
            this.getTypeLessons(this.type_id);
          }
        });
      this.moveModal = false;
    },
    // 音频移动
    moveaudioOk() {
      this.$http
        .post(this.PATH.AUDIOMOVE, {
          lesson_id: this.lessonid,
          sort_num: this.paramses.row.sort_num,
          move: parseInt(this.animal),
          audio_id: this.paramses.row.id
        })
        .then(res => {
          console.log(res);
          if (res.status == 200) {
           this.$Message.success(res.data.errmsg);
            this.getLessonsAudio();
          }
        });
      this.moveaudioModal = false;
    }
  },
  created() {
    // this.getdownlesson();
    this.getLessonsAll();
    this.getuplist();
    // this.getLessonsAudio();
  },
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
    margin-bottom: 60px;
  }
  .tip-table {
    margin: 40px 30px;
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
    right: 120px;
  }
  .zhijian-new-btn {
    height: 32px;
    line-height: 10px;
    padding: 10px 10px;
  }
  button.audiobtn {
    margin: 20px 0;
    position: relative;
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
      label {
        width: 120px;
      }
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
.con {
  margin: 20px auto;
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
