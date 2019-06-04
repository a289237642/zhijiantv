<template>
import { fail } from 'assert';
  <div id="classify">
    <div class="classify_content">
      <div class="header">
        <Icon custom="i-icon location_icon" />
        <span>分类管理</span>
        <a class="new_classify" @click="newClassify"><b class="add">+</b>新建分类</a>
      </div>
      <div class="main">
        <Row>
          <Col span="4" offset="9">视频数量</Col>
          <Col span="4" >上传时间</Col>
          <Col span="4" offset="2">操作</Col>
        </Row>
        <div class="list">
          <Row v-for="(item,index) in videoConcent" :key="index">
            <Col span="5" class="col_img">
              <img  :src="item.url == '' ? '../../assets/img/video_img.png' : item.url" alt="">
            </Col>
            <Col span="4" :title="item.title" class="video_name">{{item.title}}</Col>
            <Col span="4">{{item.num}} 个</Col>
            <Col span="4">{{item.create_time}}</Col>

            <Col  offset="3" span="3">
              <Row>
                <Col span="12" class="correct">
                  <div @click="videoCorrect">
                    <Icon custom="i-icon correct_icon" />
                    修改
                  </div>
                </Col>
                <Col span="12" class="delete">
                  <div @click="videoDelete(item.id)">
                    <Icon custom="i-icon delete_icon" />
                    删除
                  </div>
                </Col>
              </Row>
            </Col>
          </Row>
        </div>
      </div>
      <div class="footer">
        <Page :total="totals" :show-elevator='true'  :page-size='5' @on-change="flipPage" @on-page-size-change="pageSizeChange" />
      </div>
      <!-- 新建分类弹窗 -->
      <div class="mask" v-if="modal.mask"></div>
       <div class="modal-box" v-if="modal.modeBox">
         <div class="title">新建分类
           <div class="line"></div>
         </div>
         <div class="mainBox">
           <ul>
             <li class="classfy-name">
               <span>
                <Icon custom="i-icon star" />
                分类名称：
              </span>
              <input type="text" placeholder="输入分类名称" v-model='newClass'>
             </li>
             <li class="add_img_item">
            <span>
              <Icon custom="i-icon star" />
             分类图片：
            </span>
            <Upload
              multiple
              type="drag"
              :on-success='upSuccess'
              :format="['jpg','jpeg','png']"
              :on-format-error="handleFormatError"
              action="https://bjzhijian.max-tv.net.cn/api/tv1_0/up_tp_oss">
              <div class="upload_img">
                <Icon custom="i-icon upload_icon" />
                <p>+添加封面图</p>
              </div>
            </Upload>
          </li>
           </ul>
         </div>
         <!-- 两个按钮 -->
         <div class="btnBox">
           <button @click="creat">创建</button>
           <button @click="cancel">取消</button>
         </div>
      </div>
      <!-- 修改弹窗 -->
       <div class="mask" v-if="modal.modify"></div>
       <div class="modal-box" v-if="modal.modify">
         <div class="close" @click="modalModify" ></div>
         <div class="title">修改
           <div class="line"></div>
         </div>
         <div class="mainBox">
           <ul>
             <li class="classfy-name">
               <span>
                <Icon custom="i-icon star" />
                分类名称：
              </span>
              <input type="text" placeholder="输入分类名称" v-model='newClass'>
             </li>
             <li class="add_img_item1">
            <span>
              <Icon custom="i-icon star" />
             分类图片：
            </span>
            <Upload
              multiple
              type="drag"
              :on-success='upSuccess'
              :format="['jpg','jpeg','png']"
              :on-format-error="handleFormatError"
              action="https://bjzhijian.max-tv.net.cn/api/tv1_0/up_tp_oss">
              <div class="upload_img">
                <Icon custom="i-icon upload_icon" />
                <p>+添加封面图</p>
              </div>
            </Upload>
            <button class="replace">更换</button>
          </li>
          <li class="pl5" style="margin-top:30px;">
            <span>视频数量： <span class="hui">个</span></span>
          </li>
          <li class="pl5" style="margin-top:39px;">
            <span> 创建时间：<span class="hui"></span></span>
          </li>
           </ul>
         </div>
         <!-- 两个按钮 -->
         <div class="btnBox">
           <button @click="creat">创建</button>
           <button @click="cancel">取消</button>
         </div>
      </div>
      <!-- 确定删除 -->
      <div class="modal">
        <Modal
          v-model="modal.modalClick"
          title="提示"
          @on-ok="asyncOK(modal.delete)"
          >
          <p>{{modal.txtInfo}}</p>
        </Modal>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "classifyManagement",
  data() {
    return {
      // 模态框
      modal: {
        modeBox: false,
        mask: false,
        modify: false,

        modalClick: false, // 删除的视频弹窗
        delete: 1,
        txtInfo: "确定删除视频吗"
      },
      newClass: "", // 新建分类
      imgUrl: "", // 返回的图片地址
      videoConcent: [],
      classification: "", // 分类
      // 分页
      page: 1,
      pagesize: 5,
      totals: 0,

      // 视频查询参数
      vtype: "",
      is_show: "",
      title: "",
      delectId: "" // 删除视频id
    };
  },
  mounted() {
    this.getdata(this.page)
  },
  methods: {
    // 获取页面初始化数据
    getdata(page) {
      this.$http
        .post(this.URL + this.PATH.getVideoConcent, {
          page: page,
          pagesize: this.pagesize
        })
        .then(res => {
          if (res.data.errno == 0) {
            this.videoConcent = res.data.info_list;
            this.totals = res.data.vnum;
          } else {
            this.$Modal.error({
              title: "提示",
              content: res.data.errmsg
            });
          }
        });
    },
    newClassify() {
      this.modal.modeBox = true;
      this.modal.mask = true;
    },
    // 上传图片的成功
    upSuccess(response, file, fileList) {
      if (response.errno == 0) {
        this.imgUrl = response.url;
      }
    },
    creat() {
      if (this.newClass == "") {
        this.$Modal.error({
          title: "提示",
          content: "请创建分类"
        });
        return false;
      } else if (this.imgUrl == "") {
        this.$Modal.error({
          title: "提示",
          content: "请上传图片封面"
        });
        return false;
      } else {
        this.$http
          .post(this.URL + this.PATH.classifyNew, {
            title: this.newClass,
            url: this.imgUrl
          })
          .then(res => {
            if (res.data.errno == 0) {
              this.modal.modeBox = false;
              this.modal.mask = false;
              this.$Modal.success({
                title: "提示",
                content: "分类创建成功"
              });
            } else {
              this.$Modal.error({
                title: "提示",
                content: "请上传图片封面"
              });
            }
          });
      }
    },
    handleFormatError(file) {
      this.$Notice.warning({
        title: "文件格式不正确"
      });
    },
    cancel() {
      this.modal.modeBox = false;
      this.modal.mask = false;
    },
    asyncOK(parms) {
      if (parms == 1) {
        this.$http
          .post(this.URL + this.PATH.delectViedeo, { id: this.delectId })
          .then(res => {
            if (res.data.errno == 0) {
              this.$Modal.success({
                title: "提示",
                content: "删除成功"
              });
              // this.getdata(this.page)
            } else {
              this.$Modal.error({
                title: "提示",
                content: res.data.errmsg
              });
            }
          });
      }
      this.modal.modalCancel = false;
    },
    classifyChange(status, id) {
      this.$http
        .post(this.URL + this.PATH.isShowVideo, { id: id, is_show: status })
        .then(res => {
          if (res.data.errno == 0) {
            // this.getdata(this.page);
          } else {
            this.$Modal.error({
              title: "提示",
              content: res.data.errmsg
            });
          }
        });
    },
    // 获取分类
    getClassifyInfo() {
      this.$http.post(this.URL + this.PATH.classvideoList, {}).then(res => {
        if (res.data.errno == 0) {
          this.classification = res.data.info_list;
        } else {
          this.$Modal.error({
            title: "提示",
            content: res.data.errmsg
          });
        }
      });
    },
    // 获取分类点击的某一个
    classifyFilter(name) {
      this.getClassifyInfo();
      if (name == 0) {
        this.vtype = "";
        this.title = "";
        this.is_show = "";
      } else {
        this.vtype = name;
      }
      for (let i = 0; i < this.classification.length; i++) {
        if (this.classification[i].id == name) {
          this.classifyFilterTxt = this.classification[i].title;
          break;
        }
      }
      this.searchVideo(this.vtype, this.title, this.is_show);
    },
    searchVideo(vtype = "", title = "", is_show = "") {
      this.$http
        .post(this.URL + this.PATH.SEARCHVIDEO, {
          vtype: vtype,
          title: title,
          is_show: is_show,
          page: 1,
          pagesize: 5
        })
        .then(res => {
          if (res.data.errno == 0) {
            this.videoConcent = res.data.info_list;
          } else {
            this.$Modal.error({
              title: "提示",
              content: res.data.errmsg
            });
          }
        });
    },
    videoSearch() {
      this.title = this.searchTxt;
      this.searchVideo(this.vtype, this.title, this.is_show);
    },
    chosenFilter(name) {
      if (name == "001") {
        this.chosenFilterTxt = "精选";
        this.is_show = 1;
        this.searchVideo(this.vtype, this.title, this.is_show);
      }
    },
    timeFilter(name) {
      let type = "",
        vnum = "";
      for (let i = 0; i < this.sortArr.length; i++) {
        if (name == this.sortArr[i].id) {
          this.timeFilterTxt = this.sortArr[i].title;
          type = this.sortArr[i].type;
          vnum = this.sortArr[i].vnum;
          break;
        }
      }
      this.$http
        .post(this.URL + this.PATH.sortInfo, { type: type, vnum: vnum })
        .then(res => {
          if (res.data.errno == 0) {
            this.videoConcent = res.data.info_list;
          } else {
            this.$Modal.error({
              title: "提示",
              content: res.data.errmsg
            });
          }
        });
    },

    videoCorrect() {
      this.modal.modify = true;
    },
    modalModify(){
      console.log('顶顶顶')
      this.modal.modify = false;
    },
    videoDelete(id) {
      this.modal.modalClick = true;
      this.delectId = id;
    },
    flipPage(e) {
      this.page = e;
      // this.getdata(e)
    },
    pageSizeChange(pageSize) {
      alert("每页条数切换功能" + pageSize);
    }
  }
};
</script>

<style lang="less">
@base: #6461ff;
@pageBorder: #b4c7e0;
// 分类弹窗
.mask {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(55, 55, 55, 0.6);
  height: 100%;
  z-index: 1000;
}
.modal-box {
  .close{
    z-index: 99;
    position: absolute;
    right: 0;
    top:0;
    width: 50px;
    height: 50px;
    background-color: red;
  }
  position: relative;
  width: 967px;
  height: 570px;
  background-color: #fff;
  box-shadow: 0 2px 4px 5px rgba(145, 136, 212, 0.07);
  border-radius: 8px;
  padding: 10px 0 30px;
  box-sizing: border-box;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  // margin-left: -435px;
  z-index: 1001;
  .title {
    line-height: 30px;
    font-family: PingFangSC-Medium;
    font-size: 18px;
    color: #6461ff;
    padding-left: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #ccc;
    position: relative;
    .line {
      width: 72px;
      height: 2px;
      background-color: #6461ff;
      position: absolute;
      bottom: -1px;
      left: 20px;
    }
  }
  .mainBox {
    text-align: left !important;
    padding-top: 53px;
    font-size: 17.23px;
    color: #5d5bbc;
    margin-left: 40px;
  }
  .star {
    width: 13px;
    height: 13px;
    background: url("../../assets/img/star.png") no-repeat left top;
    background-size: 13px 13px;
    vertical-align: baseline;
  }
  .classfy-name {
    input {
      width: 627px;
      height: 35px;
      line-height: 35px;
      border: 1px solid #b4c7e0;
      color: #b4c7e0;
      // margin-left:5px;
      padding: 10px;
    }
  }
  .add_img_item {
    margin-top: 53px;
    .ivu-upload {
      display: inline-block;
      width: 310px;
      height: 180px;
      vertical-align: top;
      background: lighten(#d8d8d8, 10%);
      border: none;
      border-radius: 0;
      color: #ddd;
      font-size: 20px;
      .upload_img {
        position: relative;
        top: 50%;
        transform: translateY(-50%);
        .upload_icon {
          width: 55px;
          height: 55px;
          background: url("../../assets/img/upload_icon.png") no-repeat center
            center;
          background-size: 47px 37px;
          margin-bottom: 6px;
        }
      }
    }
  }
  .pl5{
      margin-left: 16px;
    }
  .add_img_item1 {
    margin-top: 53px;
    .replace {
      width: 65px;
      height: 30px;
      background: #6461ff;
      border-radius: 1px;
      margin-left: 30px;
      margin-top: 77px;
      font-family: PingFangSC-Regular;
      font-size: 16px;
      color: #ffffff;
    }
  
    .ivu-upload {
      display: inline-block;
      width: 175px;
      height: 107px;
      vertical-align: top;
      background: lighten(#d8d8d8, 10%);
      border: none;
      border-radius: 0;
      color: #ddd;
      font-size: 20px;
      .upload_img {
        position: relative;
        top: 50%;
        transform: translateY(-50%);
        .upload_icon {
          width: 55px;
          height: 55px;
          background: url("../../assets/img/upload_icon.png") no-repeat center
            center;
          background-size: 47px 37px;
          margin-bottom: 6px;
        }
      }
    }
  }
}
.btnBox {
  position: absolute;
  bottom: 40px;
  right: 40px;
}
.btnBox button {
  width: 80px;
  height: 40px;
  line-height: 40px;
  font-family: PingFangSC-Regular;
  font-size: 18px;
  background: #6461ff;
  border-radius: 1.23px;
  color: #fff;
  text-align: center;
  outline: none;
  cursor: pointer;
}
.btnBox button:nth-child(2) {
  margin-left: 43px;
  background: #f2f2f2;
  border: 1px solid #e6e6e6;
  border-radius: 1.23px;
  color: #999;
}
#classify {
  height: 100%;
}
.classify_content {
  height: 100%;
  background: #fff;
  box-shadow: 0 2px 4px 5px rgba(145, 136, 212, 0.07);
  border-radius: 8px;
  padding-top: 22px;
  position: relative;
  overflow: hidden;
  // padding-left: 10px;
  > div {
    text-align: left;
  }
  .ivu-icon-md-arrow-dropdown {
    font-size: 19px;
    color: @base;
    position: absolute;
    right: 6px;
    top: 6px;
  }
  .header {
    margin-left: 25px;
    .location_icon {
      width: 17px;
      height: 21px;
      background: url("../../assets/img/location.png") no-repeat left top;
      background-size: 17px 21px;
      vertical-align: sub;
    }
    > span {
      font-size: 24px;
      line-height: 33px;
      color: @base;
      margin-left: 7px;
    }
    .new_classify {
      float: right;
      font-size: 16px;
      line-height: 35px;
      color: @base;
      margin-right: 31px;
      .add {
        margin-right: 8px;
      }
    }
  }
  .search_box {
    margin-top: 22px;
    padding-left: 22px;
    color: @base;
    .ivu-col {
      &.ivu-col-span-3,
      &.ivu-col-span-4 {
        margin-right: 10px;
      }
      .ivu-input {
        border-radius: 0;
      }
      &.ivu-col-span-5 {
        margin-right: 10px;
      }
      &.ivu-col-span-1 {
        margin-top: -1px;
        .search_btn {
          background-image: linear-gradient(-180deg, #9d9aff 0%, @base 100%);
          font-size: 14px;
          color: #fff;
          border-radius: 0;
          border: none;
        }
      }
      &.ivu-col-span-4 {
        float: right;
        margin-right: 31px;
      }
      .ivu-dropdown {
        width: 100%;
        height: 32px;
        line-height: 32px;
        border: 1px solid #ddd;
        text-align: center;
        cursor: pointer;
        position: relative;
        a {
          color: #5d5bbc;
        }
      }
    }
  }
  .ivu-select-dropdown {
    top: 30px !important;
  }
  .main {
    margin-top: 13px;
    text-align: center;
    font-size: 14px;
    font-family: PingFangSC-Regular;
    > .ivu-row {
      height: 50px;
      line-height: 50px;
      color: @base;
      font-size: 14px;
      border: 1px solid #eee;
      border-left-style: none;
      border-right-style: none;
    }
    .list {
      .ivu-row {
        height: 136px;
        line-height: 136px;
        color: #999;
        &:not(:last-child) {
          border-bottom: 1px solid #eee;
        }
        .col_img {
          height: 136px;
          img {
            width: 200px;
            height: 107px;
            display: block;
            margin: 0 auto;
            position: relative;
            top: 50%;
            transform: translateY(-50%);
          }
        }
        .video_name {
          font-size: 18px;
          color: #000;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
        .classify_change {
          span {
            padding: 5px 12px;
            cursor: pointer;
            &.classify_up {
              background-image: linear-gradient(
                -180deg,
                #9b94ff 0%,
                #625bff 100%
              );
              color: #fff;
            }
            &.classify_down {
              background: #eee;
              color: #999;
            }
          }
        }
        .correct {
          color: @base;
        }
        .delete {
          color: #d0021b;
        }
        .i-icon {
          width: 20px;
          height: 20px;
          position: relative;
          top: -2px;
          left: -4px;
          &.correct_icon {
            background: url("../../assets/img/correct_icon.png") no-repeat left
              top;
            background-size: 100% 100%;
          }
          &.delete_icon {
            width: 15px;
            height: 19px;
            background: url("../../assets/img/delete_icon.png") no-repeat left
              top;
            background-size: 15px 19px;
          }
        }
      }
    }
  }
  .footer {
    margin-right: 48px;
    position: absolute;
    bottom: 10px;
    right: 0;
    /*button{
        height: 33px;
        line-height: 0;
        text-align: center;
        font-size: 13.54px;
        color: @base;
        !*border: 1px solid rgba(180,199,224,.3);*!
        border: 1px solid lighten(@pageBorder, 10%);
        border-radius: 0;
        &.flip_page{
          !*width: 62px;*!
        }
        &.page_num{
          !*width: 37px;*!
        }
        &.active{
          height: 35px;
          background-image: linear-gradient(-180deg, #9B94FF 0%, #625BFF 100%);
          color: #fff;
          border-right-style: none;
          border-left-style: none;
        }
      }
      .ivu-dropdown{
        width: 87px;
        height: 33px;
        line-height: 28px;
        margin-left: 12px;
        border: 1px solid lighten(@pageBorder, 10%);
        position: relative;
        a{
          height: 33px;
          line-height: 33px;
          vertical-align: top;
          color: @base;
          padding-left: 11px;
        }
        .dropdown_icon{
          top: 13px;
          right: 10px;
        }
      }*/
    .ivu-page {
      li {
        width: 37px;
        height: 35px;
        line-height: 35px;
        border-radius: 0;
        border: 1px solid lighten(@pageBorder, 10%);
        margin-right: 0;
        font-size: 14px;
        float: left;
        &.ivu-page-prev,
        &.ivu-page-next {
          width: 62px;
          height: 35px;
          line-height: 30px;
          .ivu-icon-ios-arrow-back::before {
            content: "上一页";
          }
          .ivu-icon-ios-arrow-forward::before {
            content: "下一页";
          }
        }
        a {
          color: @base;
        }
        &.ivu-page-item-active {
          background-image: linear-gradient(-180deg, #9b94ff 0%, #625bff 100%);
          border: none;
          a {
            color: #fff;
          }
        }
      }
      .ivu-page-options {
        margin-left: 12px;
        .ivu-page-options-sizer {
          margin-right: 0;
          .ivu-select {
            .ivu-select-selection {
              width: 87px;
              height: 35px;
              border: 1px solid lighten(@pageBorder, 10%);
              border-radius: 0;
              color: @base;
              .ivu-select-selected-value {
                font-size: 14px;
                line-height: 35px;
              }
              .ivu-icon-ios-arrow-down {
                font-size: 19px;
                right: 4px;
                &::before {
                  content: "\F33D";
                  color: @base;
                }
              }
            }
            .ivu-select-dropdown {
              X .ivu-select-dropdown-list {
                li {
                  width: 87px;
                  line-height: 22px;
                  border: none;
                }
              }
            }
          }
        }
      }
    }
  }
}
</style>
