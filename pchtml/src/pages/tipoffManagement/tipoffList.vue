<template>
  <div id="tipoffList">
    <h1>爆料列表</h1>
    <Input
      v-model="value"
      class="search"
      search
      enter-button="搜索"
      @on-search="search"
      @on-blur="changePages"
      placeholder="请输入搜索关键字"
    />
    <Button class="newbtn1 zhijian-new-btn" type="primary" @click="getMoreAudio">批量生成音频</Button>
    <Button class="newbtn zhijian-new-btn" type="primary" @click="downline1">批量下线</Button>

    <Tabs :value="name0" @on-click="handTabClick">
      <TabPane label="全部" name="name0">
        <Table
          class="tip-table"
          border
          :columns="columns2"
          :data="data2"
          ref="selection"
          @on-selection-change="downArc"
          @on-select-all="downlineArc"
        ></Table>
        <div class="zhijian-pagination">
          <Page
            :total="table.totalAll"
            :current="table.page"
            show-elevator
            @on-change="changePageAll"
            :pageSize="table.pagesize"
          ></Page>
        </div>
      </TabPane>
      <TabPane
        :label="item.group_name"
        :name="item.group_id + ''"
        v-for="item in onlinelist"
        :value="item.group_id"
        :key="item.group_id"
      >
        <Table
          class="tip-table"
          border
          :columns="columns1"
          :data="data1"
          ref="selection"
          @on-selection-change="downArc"
          @on-select-all="downlineArc"
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
      </TabPane>
    </Tabs>
    <!-- 是否突出显示 -->
    <Modal v-model="showModal" title="Common Modal dialog box title">
      <p class="modelp">{{confirm}}</p>
      <div class="zhijian-btn-box">
        <div class="zhijian-btn-confirm" @click="showOk">确定</div>
      </div>
    </Modal>
    <Modal v-model="configModal" title="Common Modal dialog box title" class-name="ma-edit-modal">
      <div class="edit-modal-body">
        <Icon type="android-close" @click="editModal=false"></Icon>
        <div class="title">设置</div>
        <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="100">
          <!-- <FormItem label="排序" prop="sort" v-if="showSort">
                         <Input v-model="formValidate.sort" type="text"  placeholder="请输入阿拉伯数字"></Input>
          </FormItem>-->
          <FormItem label="上线类型" prop="onlinecategory">
            <Select v-model="online" filterable multiple>
              <Option
                v-for="item in onlinelist"
                :value="item.group_id"
                :key="item.group_id"
              >{{ item.group_name }}</Option>
            </Select>
          </FormItem>
        </Form>
      </div>
      <div class="zhijian-btn-box">
        <div class="zhijian-btn-confirm" @click="configOk">确定</div>
      </div>
      <Col class="demo-spin-col" span="8" v-show="isLoding">
        <Spin size="large"></Spin>
      </Col>
    </Modal>
    <Modal v-model="modal1" title="Common Modal dialog box title">
      <p class="modelp">请确认该文章是否下线</p>
      <div class="zhijian-btn-box">
        <div class="zhijian-btn-confirm" @click="ok">确定</div>
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
export default {
  name: "tipoffList",
  data() {
    return {
      is_search: false,
      name0: "name0",
      paramses: {},
      modal1: false,
      showModal: false,
      confirm: "请确认是否取消突出显示",
      configModal: false,
      value: "",
      group_id: 1,
      onlinelist: [],
      online: [],
      onlineid: 0,
      showSort: false,
      art_detail: {},
      detailModal: false,
      checkedArc: [], //批量下线
      isLoding: false,
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
          width: 50,
          align: "center"
          // fixed:'left'
        },
        {
          title: "排序",
          key: "sort_num",
          align: "center",
          // width: 100,
          render: (h, params) => {
            return h(
              "div",
              {
                style: {
                  textAlign: "center"
                }
              },
              params.row.sort_num
            );
          }
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
                    this.detailModal = true;
                    console.log("文章详情", this.detailModal);
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
                    }),
                    h("i", {
                      attrs: {
                        class: "iconfont icon-audio"
                      },
                      style: {
                        position: "absolute",
                        right: "5px",
                        bottom: "10px",
                        display: params.row.is_read == "1" ? "normal" : "none"
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
          title: "所属分类",
          key: "group_name_list",
          // width: 120,
          align: "center",
          render: (h, params) => {
            return h("div", [h("span", {}, [params.row.group_name])]);
          }
        },
        {
          title: "上线时间",
          key: "zj_art_date",
          // width: 120,
          align: "center",
          sortable: true
        },
        {
          title: "操作",
          key: "action",
          // width: 450,
          align: "center",
          // fixed:'right',
          render: (h, params) => {
            return h("div", [
              // h(
              //   "Spin",
              //   {
              //     props: {},
              //     style: {
              //       display:
              //         params.row.article_id == this.onlineid
              //           ? "inline-block"
              //           : "none",
              //       border: "1px solid black",
              //       borderRadius: "5px",
              //       padding: "1px 10px",
              //       marginRight: "5px"
              //     }
              //   },
              //   "操作中..."
              // ),
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small",
                    class: "btn"
                  },
                  style: {
                    background: params.row.is_read == "1" ? "white" : "black",
                    border:
                      params.row.is_read == "1" ? "1px solid black" : "none",
                    color: params.row.is_read == "1" ? "black" : "white",
                    marginRight: "5px"
                    // display:
                    //   params.row.article_id == this.onlineid
                    //     ? "none"
                    //     : "inline-block"
                  },
                  on: {
                    click: () => {
                      this.paramses = params;
                      this.onlineid = params.row.article_id;
                      this.$Spin.show({
                        render: h => {
                          return h("div", [
                            h("Icon", {
                              class: "demo-spin-icon-load",
                              props: {
                                type: "ios-loading",
                                size: 18
                              }
                            }),
                            h("div", "操作中...")
                          ]);
                        }
                      });
                      this.getAudio();
                    }
                  }
                },
                params.row.is_read == "1" ? "取消音频" : "生成音频"
              ),
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small",
                    class: "btn"
                  },
                  style: {
                    background: params.row.is_big == "1" ? "white" : "black",
                    border:
                      params.row.is_big == "1" ? "1px solid black" : "none",
                    color: params.row.is_big == "1" ? "black" : "white",
                    marginRight: "5px"
                  },
                  on: {
                    click: () => {
                      this.paramses = params;
                      this.confirm =
                        params.row.is_big == "1"
                          ? "请确认是否取消突出显示"
                          : "请确认是否突出显示";
                      this.showModal = true;
                    }
                  }
                },
                params.row.is_big == "1" ? "取消显示" : "突出显示"
              ),
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small",
                    class: "btn"
                  },
                  style: {
                    background: "black",
                    border: "none",
                    marginRight: "5px"
                  },
                  on: {
                    click: () => {
                      this.paramses = params;
                      // this.showSort = true;
                      this.getgroups();
                      this.onlineid = params.row.article_id;
                      // this.configModal = true;
                      // this.online = [];
                      // this.online.push(this.group_id);

                      this.getbelongcate(params.row);
                    }
                  }
                },
                "设置"
              ),
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small",
                    class: "btn"
                  },
                  style: {
                    background: "black",
                    border: "none",
                    marginRight: "30px"
                  },
                  on: {
                    click: () => {
                      this.paramses = params;
                      this.checkedArc.push(params.row.article_id);
                      this.modal1 = true;
                    }
                  }
                },
                "下线"
              )
            ]);
          }
        }
      ],
      columns2: [
        {
          type: "selection",
          title: "全选",
          width: 50,
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
                    this.detailModal = true;
                    console.log("文章详情", this.detailModal);
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
                    }),
                    h("i", {
                      attrs: {
                        class: "iconfont icon-audio"
                      },
                      style: {
                        position: "absolute",
                        right: "5px",
                        bottom: "10px",
                        width: "20px",
                        height: "20px",
                        color: "#fff",
                        zIndex: 9,
                        display: params.row.is_read == "1" ? "normal" : "none"
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
          title: "所属分类",
          key: "group_name_list",
          // width: 200,
          render: (h, params) => {
            return h("div", [h("span", {}, params.row.group_name_list + " ")]);
          }
        },
        {
          title: "上线时间",
          key: "wechat_art_date",
          // width: 200,
          sortable: true
        },
        {
          title: "操作",
          key: "action",
          // width: 450,
          align: "center",
          render: (h, params) => {
            return h("div", [
              // h(
              //   "Spin",
              //   {
              //     props: {},
              //     style: {
              //       display:
              //         params.row.article_id == this.onlineid
              //           ? "inline-block"
              //           : "none",
              //       border: "1px solid black",
              //       borderRadius: "5px",
              //       padding: "1px 10px",
              //       marginRight: "5px"
              //     }
              //   },
              //   "操作中..."
              // ),
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small",
                    class: "btn"
                  },
                  style: {
                    background: params.row.is_read == "1" ? "white" : "black",
                    border:
                      params.row.is_read == "1" ? "1px solid black" : "none",
                    color: params.row.is_read == "1" ? "black" : "white",
                    marginRight: "5px"
                    // display:
                    //   params.row.article_id == this.onlineid
                    //     ? "none"
                    //     : "inline-block"
                  },
                  on: {
                    click: () => {
                      this.paramses = params;
                      this.onlineid = params.row.article_id;
                      this.$Spin.show({
                        render: h => {
                          return h("div", [
                            h("Icon", {
                              class: "demo-spin-icon-load",
                              props: {
                                type: "ios-loading",
                                size: 18
                              }
                            }),
                            h("div", "操作中...")
                          ]);
                        }
                      });
                      this.getAudio();
                    }
                  }
                },
                params.row.is_read == "1" ? "取消音频" : "生成音频"
              ),
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small",
                    class: "btn"
                  },
                  style: {
                    background: params.row.is_big == "1" ? "white" : "black",
                    border:
                      params.row.is_big == "1" ? "1px solid black" : "none",
                    color: params.row.is_big == "1" ? "black" : "white",
                    marginRight: "5px"
                  },
                  on: {
                    click: () => {
                      this.paramses = params;
                      this.confirm =
                        params.row.is_big == "1"
                          ? "请确认是否取消突出显示"
                          : "请确认是否突出显示";
                      this.showModal = true;
                    }
                  }
                },
                params.row.is_big == "1" ? "取消显示" : "突出显示"
              ),
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small",
                    class: "btn"
                  },
                  style: {
                    background: "black",
                    border: "none",
                    marginRight: "5px"
                  },
                  on: {
                    click: () => {
                      // this.showSort = false;
                      // this.paramses = params;
                      // this.configModal = true;
                      // this.online = []; //先初始化
                      this.onlineid = params.row.article_id;
                      this.getgroups();
                      this.getbelongcate(params.row); //绑定默认分类
                    }
                  }
                },
                "设置"
              ),
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small",
                    class: "btn"
                  },
                  style: {
                    background: "black",
                    border: "none",
                    marginRight: "30px"
                  },
                  on: {
                    click: () => {
                      this.paramses = params;
                      this.checkedArc.push(params.row.article_id);
                      this.modal1 = true;
                    }
                  }
                },
                "下线"
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
    this.getArticlesAll();
    this.getgroups();
  },
  methods: {
    getArticlesAll() {
      this.$http
        .post(this.PATH.ARTICLES, {
          page: this.table.page,
          pagesize: this.table.pagesize,
          is_show: 1
        })
        .then(res => {
          console.log(res, "data2");
          if (res.status == 200) {
            this.data2 = res.data.data;
            this.table.totalAll = res.data.count;
          }
        });
    },
    // 获取全部文章
    getArticles() {
      this.$http
        .post(this.PATH.ARTICLEGROUP, {
          group_id: this.group_id,
          page: this.table.page,
          pagesize: this.table.pagesize
        })
        .then(res => {
          console.log(res, "data1");
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
      this.group_id = groupid;
      this.changePages();
      if (groupid == "name0") {
        this.getArticlesAll();
      } else {
        this.getArticles();
      }
    },
    // 全选拿到选中的文章id
    downlineArc(selection) {
      this.checkedArc = [];
      selection.forEach(v => {
        this.checkedArc.push(v.article_id);
      });
      // console.log(this.checkedArc,'全选');
    },
    // 多选拿到选中的文章id
    downArc(selection) {
      this.checkedArc = [];
      selection.forEach(v => {
        this.checkedArc.push(v.article_id);
      });
      console.log(this.checkedArc, "多选");
    },
    //批量下线
    downline1() {
      let paramss = {};
      let list = this.checkedArc;
      // console.log(list);
      // list.push(paramses.row.article_id);
      if (this.name0 === "name0") {
        paramss = {
          article_id_list: list
        };
      } else {
        paramss = {
          article_id_list: list,
          group_id: this.group_id
        };
      }
      this.$http.post(this.PATH.DOWNLINE, paramss).then(res => {
        console.log(res.data.errmsg);
        if (res.status == 200) {
          this.$Modal.error({
            width: 360,
            content: res.data.errmsg
          });
          if (this.is_search) {
            this.search();
          } else if (this.name0 === "name0") {
            this.getArticlesAll();
          } else {
            this.getArticles();
          }
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
      // list.push(paramses.row.article_id);
      if (paramses.row.wechat_art_date === undefined) {
        paramss = {
          article_id_list: list,
          group_id: this.group_id
        };
      } else {
        paramss = {
          article_id_list: list
        };
      }
      this.$http.post(this.PATH.DOWNLINE, paramss).then(res => {
        console.log(res);
        if (res.status == 200) {
          this.$Modal.error({
            width: 360,
            content: res.data.errmsg
          });
          if (this.is_search) {
            this.search();
          } else if (paramses.row.wechat_art_date === undefined) {
            this.getArticles();
          } else {
            this.getArticlesAll();
          }
          this.checkedArc = [];
        }
      });
    },
    //确定/取消突出显示
    showOk() {
      let paramss = {};
      let index = this.paramses.index;
      let isbig = this.paramses.row.is_big;
      paramss = {
        article_id: this.paramses.row.article_id
      };
      this.$http.post(this.PATH.SHOWBIG, paramss).then(res => {
        if (res.status == 200) {
          if (this.is_search) {
            this.search();
          } else if (this.paramses.row.wechat_art_date === undefined) {
            this.data1[index].is_big = isbig == "0" ? "1" : "0";
          } else {
            this.data2[index].is_big = isbig == "0" ? "1" : "0";
          }
        }
      });
      this.showModal = false; //隐藏弹框
    },
    ok() {
      this.modal1 = false;
      // let paramses = this.paramses;
      this.downline();
    },
    changePages() {
      this.table.page = 1;
    },
    search() {
      this.is_search = true;
      this.name0 = "name0";
      this.$http
        .post(this.PATH.ONLINESearch, {
          words: this.value,
          // is_show: this.table.is_show,
          page: this.table.page,
          pagesize: this.table.pagesize
        })
        .then(res => {
          console.log(res);
          if (res.status == 200) {
            this.data2 = res.data.data;
            this.table.totalAll = res.data.count;
          }
        });
    },
    changePage(page) {
      this.table.page = page;
      this.getArticles();
    },
    changePageAll(page) {
      this.table.page = page;
      if (this.is_search) {
        this.search();
      } else {
        this.getArticlesAll();
      }
    },
    //获取爆料类型列表
    getgroups() {
      this.$http.get(this.PATH.PCGROUPS).then(res => {
        if (res.data.errno == 0) {
          this.onlinelist = res.data.data.map(function(item) {
            return {
              group_id: parseInt(item.group_id.slice(2)), //把分类ID处理成数字
              group_name: item.group_name
            };
          });
          this.online.push(this.group_id);
        } else {
          this.$Modal.error({
            width: 360,
            content: res.data.errmsg
          });
        }
      });
    },

    //获取该文章所在上线类型
    getbelongcate(row) {
      console.log(row, "roe");
      this.configModal = true;
      this.isLoding = true;
      this.online = []; //先初始化
      this.onlineid = row.article_id;
      // this.formValidate.sort = row.sort_num; //绑定原来序号
      this.$http
        .post(this.PATH.CURRENTGROUP, {
          article_id: row.article_id
        })
        .then(res => {
          console.log(res, "设置");
          if (res.data.errno == 0) {
            let that = this;
            res.data.data.forEach(v => {
              that.online.push(v.group_id); //双向绑定
            });
            setTimeout(function() {
              that.isLoding = false;
            }, 600);
          } else {
            this.$Modal.error({
              width: 360,
              content: res.data.errmsg
            });
          }
        });
    },
    //确定保存设置
    configOk() {
      this.$http
        .post(this.PATH.SETARTICLE, {
          article_id: this.onlineid,
          group_id_list: this.online
          // sort_num: parseInt(this.formValidate.sort)
        })
        .then(res => {
          // console.log(res);
          if (res.status == 200) {
            this.$Modal.error({
              width: 360,
              content: res.data.errmsg
            });
            if (this.is_search) {
              this.search();
            } else if (this.paramses.row.wechat_art_date === undefined) {
              this.getArticles();
            } else {
              this.getArticlesAll();
            }
          }
        });
      this.configModal = false;
      this.formValidate.sort = "";
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
    },
    // 文章转语音
    getAudio() {
      let index = this.paramses.index;
      let isread = this.paramses.row.is_read;
      console.log(this.paramses.row, "isread");
      let list = [];
      list.push(this.onlineid);
      this.$http
        .post(this.PATH.GETAUDIO, {
          article_id_list: list,
          is_read: isread
          // data: this.paramses.row.content
        })
        .then(res => {
          console.log(res);
          if (res.status == 200) {
            // this.onlineid = ""; //为了取消操作中的显示
            this.$Spin.hide();
            this.$Message.info(res.data.errmsg);
            if (res.data.errno == 0) {
              if (this.is_search) {
                this.search();
              } else if (this.paramses.row.wechat_art_date === undefined) {
                this.data1[index].is_read = isread == "1" ? "0" : "1";
              } else {
                this.data2[index].is_read = isread == "1" ? "0" : "1";
              }
            }
          }
        });
    },
    // 文章批量转语音
    getMoreAudio() {
      this.$http
        .post(this.PATH.GETAUDIO, {
          // article_id: this.onlineid,
          article_id_list: this.checkedArc
          // data: this.paramses.row.content
        })
        .then(res => {
          console.log(res);
          if (res.status == 200) {
            // this.onlineid = ""; //为了取消操作中的显示
            this.$Spin.hide();
            this.$Message.info(res.data.errmsg);
            if (res.data.errno == 0) {
              if (this.is_search) {
                this.search();
              } else if (this.name0 === "name0") {
                this.getArticlesAll();
              } else {
                this.getArticles();
              }
              this.checkedArc = [];
            }
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
  background: #fff;
  position: relative;
  overflow: scroll;
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
.demo-spin-col {
  position: absolute;
  top: 50%;
  left: 60%;
  transform: translate(-50%, -60%);
}
</style>
