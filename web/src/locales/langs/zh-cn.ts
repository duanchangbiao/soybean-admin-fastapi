const local: App.I18n.Schema = {
  system: {
    title: '管理后台',
    updateTitle: '系统版本更新通知',
    updateContent: '检测到系统有新版本发布，是否立即刷新页面？',
    updateConfirm: '立即刷新',
    updateCancel: '稍后再说'
  },
  common: {
    action: '操作',
    add: '新增',
    synchronous:'同步',
    addSuccess: '添加成功',
    backToHome: '返回首页',
    batchDelete: '批量删除',
    batchApprove: '批量通过',
    batchReject: '批量拒绝',
    cancel: '取消',
    close: '关闭',
    check: '勾选',
    expandColumn: '展开列',
    columnSetting: '列设置',
    config: '配置',
    confirm: '确认',
    delete: '删除',
    execute: '执行',
    deleteSuccess: '删除成功',
    confirmDelete: '确认删除吗？',
    approve: '通过',
    approveSuccess: '通过成功',
    confirmApprove: '确认通过吗？',
    reject: '拒绝',
    rejectSuccess: '拒绝成功',
    confirmReject: '确认拒绝吗？',
    edit: '编辑',
    view: '查看',
    warning: '警告',
    error: '错误',
    index: '序号',
    keywordSearch: '请输入关键词搜索',
    logout: '退出登录',
    logoutConfirm: '确认退出登录吗？',
    lookForward: '敬请期待',
    modify: '修改',
    modifySuccess: '修改成功',
    noData: '无数据',
    operate: '操作',
    pleaseCheckValue: '请检查输入的值是否合法',
    refresh: '刷新',
    refreshAPI: '刷新API',
    reset: '重置',
    search: '搜索',
    switch: '切换',
    tip: '提示',
    trigger: '触发',
    update: '更新',
    updateSuccess: '更新成功',
    userCenter: '个人中心',
    yesOrNo: {
      yes: '是',
      no: '否'
    }
  },
  request: {
    logout: '请求失败后登出用户',
    logoutMsg: '用户状态失效，请重新登录',
    logoutWithModal: '请求失败后弹出模态框再登出用户',
    logoutWithModalMsg: '用户状态失效，请重新登录',
    refreshToken: '请求的token已过期，刷新token',
    tokenExpired: 'token已过期'
  },
  theme: {
    themeSchema: {
      title: '主题模式',
      light: '亮色模式',
      dark: '暗黑模式',
      auto: '跟随系统'
    },
    grayscale: '灰色模式',
    colourWeakness: '色弱模式',
    layoutMode: {
      title: '布局模式',
      vertical: '左侧菜单模式',
      'vertical-mix': '左侧菜单混合模式',
      horizontal: '顶部菜单模式',
      'horizontal-mix': '顶部菜单混合模式',
      reverseHorizontalMix: '一级菜单与子级菜单位置反转'
    },
    recommendColor: '应用推荐算法的颜色',
    recommendColorDesc: '推荐颜色的算法参照',
    themeColor: {
      title: '主题颜色',
      primary: '主色',
      info: '信息色',
      success: '成功色',
      warning: '警告色',
      error: '错误色',
      followPrimary: '跟随主色'
    },
    scrollMode: {
      title: '滚动模式',
      wrapper: '外层滚动',
      content: '主体滚动'
    },
    page: {
      animate: '页面切换动画',
      mode: {
        title: '页面切换动画类型',
        'fade-slide': '滑动',
        fade: '淡入淡出',
        'fade-bottom': '底部消退',
        'fade-scale': '缩放消退',
        'zoom-fade': '渐变',
        'zoom-out': '闪现',
        none: '无'
      }
    },
    fixedHeaderAndTab: '固定头部和标签栏',
    header: {
      height: '头部高度',
      breadcrumb: {
        visible: '显示面包屑',
        showIcon: '显示面包屑图标'
      }
    },
    tab: {
      visible: '显示标签栏',
      cache: '标签栏信息缓存',
      height: '标签栏高度',
      mode: {
        title: '标签栏风格',
        chrome: '谷歌风格',
        button: '按钮风格'
      }
    },
    sider: {
      inverted: '深色侧边栏',
      width: '侧边栏宽度',
      collapsedWidth: '侧边栏折叠宽度',
      mixWidth: '混合布局侧边栏宽度',
      mixCollapsedWidth: '混合布局侧边栏折叠宽度',
      mixChildMenuWidth: '混合布局子菜单宽度'
    },
    footer: {
      visible: '显示底部',
      fixed: '固定底部',
      height: '底部高度',
      right: '底部局右'
    },
    watermark: {
      visible: '显示全屏水印',
      text: '水印文本'
    },
    themeDrawerTitle: '主题配置',
    pageFunTitle: '页面功能',
    resetCacheStrategy: {
      title: '重置缓存策略',
      close: '关闭页面',
      refresh: '刷新页面'
    },
    configOperation: {
      copyConfig: '复制配置',
      copySuccessMsg: '复制成功，请替换 src/theme/settings.ts 中的变量 themeSettings',
      resetConfig: '重置配置',
      resetSuccessMsg: '重置成功'
    }
  },
  route: {
    login: '登录',
    403: '无权限',
    404: '页面不存在',
    500: '服务器错误',
    'iframe-page': '外链页面',
    home: '首页',
    document: '文档',
    document_project: '项目文档',
    'company-info': '数据中心',
    monitor: '监控中心',
    monitor_aft: 'AFFA/AFT监控中心',
    monitor_mor: 'MOR5/MOR9监控中心',
    monitor_nsw: 'NSW 监控中心',
    account: '账号中心',
    'document_project-link': '项目文档(外链)',
    document_vue: 'Vue文档',
    document_vite: 'Vite文档',
    document_unocss: 'UnoCSS文档',
    document_naive: 'Naive UI文档',
    document_antd: 'Ant Design Vue文档',
    document_alova: 'Alova文档',
    'user-center': '个人中心',
    manage: '系统管理',
    manage_log: '日志管理',
    manage_api: 'API管理',
    manage_user: '用户管理',
    'manage_user-detail': '用户详情',
    manage_role: '角色管理',
    manage_menu: '菜单管理',
    exception: '异常页',
    exception_403: '403',
    exception_404: '404',
    exception_500: '500',
    plugin: '插件示例',
    plugin_copy: '剪贴板',
    plugin_charts: '图表',
    plugin_charts_echarts: 'ECharts',
    plugin_charts_antv: 'AntV',
    plugin_charts_vchart: 'VChart',
    plugin_editor: '编辑器',
    plugin_editor_quill: '富文本编辑器',
    plugin_editor_markdown: 'MD 编辑器',
    plugin_icon: '图标',
    plugin_map: '地图',
    plugin_print: '打印',
    plugin_swiper: 'Swiper',
    plugin_video: '视频',
    plugin_barcode: '条形码',
    plugin_pinyin: '拼音',
    plugin_excel: 'Excel',
    plugin_pdf: 'PDF 预览',
    plugin_gantt: '甘特图',
    plugin_gantt_dhtmlx: 'dhtmlxGantt',
    plugin_gantt_vtable: 'VTableGantt',
    plugin_typeit: '打字机',
    plugin_tables: '表格',
    plugin_tables_vtable: 'VTable'
  },
  page: {
    login: {
      common: {
        loginOrRegister: '登录 / 注册',
        userNamePlaceholder: '请输入用户名',
        phonePlaceholder: '请输入手机号',
        codePlaceholder: '请输入验证码',
        passwordPlaceholder: '请输入密码',
        confirmPasswordPlaceholder: '请再次输入密码',
        codeLogin: '验证码登录',
        confirm: '确定',
        back: '返回',
        validateSuccess: '验证成功',
        loginSuccess: '登录成功',
        welcomeBack: '欢迎回来，{nickName} ！'
      },
      pwdLogin: {
        title: '密码登录',
        rememberMe: '记住我',
        forgetPassword: '忘记密码？',
        register: '注册账号',
        otherAccountLogin: '其他账号登录',
        otherLoginMode: '其他登录方式',
        superAdmin: '超级管理员',
        admin: '管理员',
        user: '普通用户'
      },
      codeLogin: {
        title: '验证码登录',
        getCode: '获取验证码',
        reGetCode: '{time}秒后重新获取',
        sendCodeSuccess: '验证码发送成功',
        imageCodePlaceholder: '请输入图片验证码'
      },
      register: {
        title: '注册账号',
        agreement: '我已经仔细阅读并接受',
        protocol: '《用户协议》',
        policy: '《隐私权政策》'
      },
      resetPwd: {
        title: '重置密码'
      },
      bindWeChat: {
        title: '绑定微信'
      }
    },
    home: {
      branchDesc:
        '为了方便大家开发和更新合并，我们对main分支的代码进行了精简，只保留了首页菜单，其余内容已移至example分支进行维护。预览地址显示的内容即为example分支的内容。',
      greeting: '早安，{userName}, 今天又是充满活力的一天!',
      weatherDesc: '今日多云转晴，20℃ - 25℃!',
      projectCount: '项目数',
      todo: '待办',
      message: '消息',
      downloadCount: '下载量',
      registerCount: '注册量',
      schedule: '作息安排',
      study: '学习',
      work: '工作',
      rest: '休息',
      entertainment: '娱乐',
      visitCount: '访问量',
      turnover: '成交额',
      dealCount: '成交量',
      projectNews: {
        title: '项目动态',
        moreNews: '更多动态',
        desc1: 'Soybean 在2021年5月28日创建了开源项目 soybean-admin!',
        desc2: 'Yanbowe 向 soybean-admin 提交了一个bug，多标签栏不会自适应。',
        desc3: 'Soybean 准备为 soybean-admin 的发布做充分的准备工作!',
        desc4: 'Soybean 正在忙于为soybean-admin写项目说明文档！',
        desc5: 'Soybean 刚才把工作台页面随便写了一些，凑合能看了！'
      },
      creativity: '创意'
    },
    function: {
      tab: {
        tabOperate: {
          title: '标签页操作',
          addTab: '添加标签页',
          addTabDesc: '跳转到关于页面',
          closeTab: '关闭标签页',
          closeCurrentTab: '关闭当前标签页',
          closeAboutTab: '关闭"关于"标签页',
          addMultiTab: '添加多标签页',
          addMultiTabDesc1: '跳转到多标签页页面',
          addMultiTabDesc2: '跳转到多标签页页面(带有查询参数)'
        },
        tabTitle: {
          title: '标签页标题',
          changeTitle: '修改标题',
          change: '修改',
          resetTitle: '重置标题',
          reset: '重置'
        }
      },
      multiTab: {
        routeParam: '路由参数',
        backTab: '返回 function_tab'
      },
      toggleAuth: {
        toggleAccount: '切换账号',
        authHook: '权限钩子函数 `hasAuth`',
        superAdminVisible: '超级管理员可见',
        adminVisible: '管理员可见',
        adminOrUserVisible: '管理员和用户可见'
      },
      request: {
        repeatedErrorOccurOnce: '重复请求错误只出现一次',
        repeatedError: '重复请求错误',
        repeatedErrorMsg1: '自定义请求错误 1',
        repeatedErrorMsg2: '自定义请求错误 2'
      }
    },
    manage: {
      common: {
        statusType: {
          enable: '启用',
          disable: '禁用'
        },
        businessStatus: {
          update: '有更新',
          latest: '已最新',
          dispose: '已处理',
        },
        account: {
          mor5: 'MOR5',
          mor9: 'MOR9',
          aft: 'AFT',
          affa: 'AFFA',
          nsw: 'NSW'
        },
        executeSuccess: '执行成功!'
      },
      role: {
        title: '角色列表',
        roleName: '角色名称',
        roleCode: '角色编码',
        rolestatusType: '角色状态',
        roleDesc: '角色描述',
        menuAuth: '菜单权限',
        buttonAuth: '按钮权限',
        apiAuth: 'API权限',
        form: {
          roleName: '请输入角色名称',
          roleCode: '请输入角色编码',
          rolestatusType: '请选择角色状态',
          roleDesc: '请输入角色描述'
        },
        addRole: '新增角色',
        editRole: '编辑角色'
      },
      log: {
        title: '日志列表',
        logType: '日志类型',
        byUser: '用户',
        logDetailType: '日志详细',
        createTime: '创建时间',
        requestDomain: '请求域名',
        requestPath: '请求路径',
        responseCode: '业务状态码',
        xRequestId: 'x-request-id',
        requestParams: '请求参数',
        responseData: '请求体数据',
        userAgent: 'userAgent',
        processTime: '请求处理时间(s)',
        ipAddress: '来源IP地址',
        form: {
          logType: '请选择日志类型',
          byUser: '请输入用户',
          logDetailType: '请选择日志详细',
          requestPath: '请输入请求路径',
          createTime: '请选择创建时间',
          responseCode: '请输入业务状态码'
        },
        viewLog: '查看日志',
        logDetailTypes: {
          SystemStart: '系统启动',
          SystemStop: '系统关闭',
          UserLoginSuccess: '用户登录成功',
          UserAuthRefreshTokenSuccess: '用户认证刷新令牌成功',
          UserLoginGetUserInfo: '用户登录获取用户信息',
          UserLoginUserNameVaild: '用户登录用户名有效',
          UserLoginErrorPassword: '用户登录密码错误',
          UserLoginForbid: '用户登录禁止',
          ApiGetList: '获取接口列表',
          ApiGetTree: '获取接口树',
          ApiRefresh: '刷新接口',
          ApiGetOne: '获取单个接口',
          ApiCreateOne: '创建单个接口',
          ApiUpdateOne: '更新单个接口',
          ApiDeleteOne: '删除单个接口',
          ApiBatchDelete: '批量删除接口',
          MenuGetList: '获取菜单列表',
          MenuGetTree: '获取菜单树',
          MenuGetPages: '获取菜单页面',
          MenuGetButtonsTree: '获取菜单按钮树',
          MenuGetOne: '获取单个菜单',
          MenuCreateOne: '创建单个菜单',
          MenuUpdateOne: '更新单个菜单',
          MenuDeleteOne: '删除单个菜单',
          MenuBatchDeleteOne: '批量删除菜单',
          RoleGetList: '获取角色列表',
          RoleGetMenus: '获取角色菜单',
          RoleUpdateMenus: '更新角色菜单',
          RoleGetButtons: '获取角色按钮',
          RoleUpdateButtons: '更新角色按钮',
          RoleGetApis: '获取角色接口',
          RoleUpdateApis: '更新角色接口',
          RoleGetOne: '获取单个角色',
          RoleCreateOne: '创建单个角色',
          RoleUpdateOne: '更新单个角色',
          RoleDeleteOne: '删除单个角色',
          RoleBatchDeleteOne: '批量删除角色',
          UserGetList: '获取用户列表',
          UserGetOne: '获取单个用户',
          UserCreateOne: '创建单个用户',
          UserUpdateOne: '更新单个用户',
          UserDeleteOne: '删除单个用户',
          UserBatchDeleteOne: '批量删除用户'
        },
        logTypes: {
          ApiLog: 'API日志',
          UserLog: '用户日志',
          AdminLog: '管理日志',
          SystemLog: '系统日志'
        }
      },
      api: {
        title: 'API列表',
        path: 'API路径',
        method: '请求方式',
        summary: 'API简介',
        tags: 'Tags',
        statusType: 'API状态',
        form: {
          path: '请输入API路径',
          method: '请选择请求方式',
          summary: '请输入API简介',
          tags: '请输入Tags',
          statusType: '请选择API状态'
        },
        addApi: '新增API',
        editApi: '编辑API',
        methods: {
          GET: 'GET',
          POST: 'POST',
          PUT: 'PUT',
          PATCH: 'PATCH',
          DELETE: 'DELETE'
        }
      },
      user: {
        title: '用户列表',
        userName: '用户名',
        password: '密码',
        userGender: '性别',
        nickName: '昵称',
        userPhone: '手机号',
        userEmail: '邮箱',
        userStatusType: '用户状态',
        userRole: '用户角色',
        form: {
          userName: '请输入用户名',
          password: '请输入密码',
          userGender: '请选择性别',
          nickName: '请输入昵称',
          userPhone: '请输入手机号',
          userEmail: '请输入邮箱',
          userStatusType: '请选择用户状态',
          userRole: '请选择用户角色'
        },
        addUser: '新增用户',
        editUser: '编辑用户',
        gender: {
          male: '男',
          female: '女',
          unknow: '未知'
        }
      },
      menu: {
        home: '首页',
        title: '菜单列表',
        id: 'ID',
        parentId: '父级菜单ID',
        menuType: '菜单类型',
        menuName: '菜单名称',
        routeName: '路由名称',
        routePath: '路由路径',
        pathParam: '路径参数',
        layout: '布局',
        page: '页面组件',
        i18nKey: '国际化key',
        icon: '图标',
        localIcon: '本地图标',
        iconTypeTitle: '图标类型',
        order: '排序',
        constant: '常量路由',
        keepAlive: '缓存路由',
        href: '外链',
        hideInMenu: '隐藏菜单',
        activeMenu: '高亮的菜单',
        multiTab: '支持多页签',
        fixedIndexInTab: '固定在页签中的序号',
        query: '路由参数',
        button: '按钮',
        buttonCode: '按钮编码',
        buttonDesc: '按钮描述',
        menuStatusType: '菜单状态',
        form: {
          home: '请选择首页',
          menuType: '请选择菜单类型',
          menuName: '请输入菜单名称',
          routeName: '请输入路由名称',
          routePath: '请输入路由路径',
          pathParam: '请输入路径参数',
          page: '请选择页面组件',
          layout: '请选择布局组件',
          i18nKey: '请输入国际化key',
          icon: '请输入图标',
          localIcon: '请选择本地图标',
          order: '请输入排序',
          keepAlive: '请选择是否缓存路由',
          href: '请输入外链',
          hideInMenu: '请选择是否隐藏菜单',
          activeMenu: '请选择高亮的菜单的路由名称',
          multiTab: '请选择是否支持多标签',
          fixedInTab: '请选择是否固定在页签中',
          fixedIndexInTab: '请输入固定在页签中的序号',
          queryKey: '请输入路由参数Key',
          queryValue: '请输入路由参数Value',
          button: '请选择是否按钮',
          buttonCode: '请输入按钮编码',
          buttonDesc: '请输入按钮描述',
          menuStatusType: '请选择菜单状态'
        },
        addMenu: '新增菜单',
        editMenu: '编辑菜单',
        addChildMenu: '新增子菜单',
        type: {
          directory: '目录',
          menu: '菜单'
        },
        iconType: {
          iconify: 'iconify图标',
          local: '本地图标'
        }
      }
    },
    business: {
      license: {
        title: '工业产品标准许可证信息',
        companyName: '工厂名称',
        companyAddress: '公司地址',
        factoryAddress: '工厂地址',
        factoryRegistrationNumber: '工厂注册号',
        issuanceTime: '发放日期',
        licenseCategory: '类别',
        licenseCompany: '授权公司',
        licenseId: '许可证编号',
        licenseType: 'TIS编号',
        taxIdentificationNumber: '纳税人标识',
        ctime: '创建时间',
        mtime: '修改时间',
        details: '说明',
        form: {
          companyName: '请输入工厂名称',
          companyAddress: '请输入公司地址',
          factoryAddress: '请输入工厂地址',
          factoryRegistrationNumber: '请输入工厂注册号',
          issuanceTime: '请输入发放日期',
          licenseCategory: '请输入类别',
          licenseCompany: '请输入授权公司',
          licenseId: '请输入许可证编号',
          licenseType: '请输入TIS编号',
          taxIdentificationNumber: '请输入纳税人标识',
          details: '请输入说明',
        },
        addLicense: '添加许可信息',
        editLicense: '编辑许可信息',
      },
      aft: {
        id: '编号',
        title: 'AFT/AFFA 模块数据中心',
        applyNumber: '申请编号',
        tisCode: 'TIS CODE',
        standardName: '标准信息',
        applyLicense: '申请许可证',
        applyDate: '申请日期',
        applyStatus: '申请状态',
        accountNumber: '账号信息',
        nickName: '昵称',
        aftType: '类型',
        aftTypeInfo: {
          aft: 'AFT',
          affa: 'AFFA'
        },
        updateStatus: '更新状态',
        sort: '排序',
        remark: '备注',
        passTime: '通过时间',
        ctime: '创建时间',
        mtime: '更新时间',
        form: {
          applyStatus: '请输入申请状态',
          applyNumber: '请输入申请编号',
          tisCode: '请输入TIS CODE',
          standardName: '请输入标准信息',
          applyLicense: '请输入申请许可证',
          applyDate: '请输入申请日期',
          accountNumber: '请输入账号信息',
          nickName: '请输入昵称',
          aftType: '请输入类型',
          updateStatus: '请输入更新状态',
          sort: '请输入排序数字',
          remark: '请输入备注信息',
          passTime: '请输入通过时间',
        },
        addAft: '添加AFT/AFFA',
        editAft: '编辑AFT/AFFA',
      },
      mor: {
        id: '编号',
        title: 'MOR 模块数据中心',
        companyName: '操作人',
        applyNumber: '申请编号',
        tisCode: 'TIS CODE',
        standardName: '标准信息',
        applyLicense: '申请许可证',
        applyDate: '申请日期',
        applyTaxNumber: '税号',
        updateStatus: '更新状态',
        applyStatus: '申请状态',
        accountNumber: '账号信息',
        nickName: '昵称',
        morType: '类型',
        ctime: '创建时间',
        mtime: '更新时间',
        sort: '排序',
        morTypeStatus: {
          mor5: 'Mor5',
          mor9: 'Mor9',
        },
        remark: '备注',
        nickname: '昵称',
        form: {
          companyName: '请输入操作人信息',
          applyNumber: '请输入申请编号',
          tisCode: '请输入TIS Code 信息',
          standardName: '请输入标准信息',
          applyLicense: '请输入申请许可证',
          applyDate: '请输入申请日期',
          applyTaxNumber: '请输入税号',
          applyStatus: '请输入申请状态',
          morType: '请选择类型',
          updateStatus: '请选择更新情况',
          accountNumber: '请输入账号信息',
          nickname: '请输入昵称',
          sort: '请输入排序数字',
          remark: '请输入备注信息'
        },
        addMor: '添加MOR5/MOR9',
        editMor: '编辑MOR5/MOR9',
      },
      nsw: {
        id: '编号',
        title: 'NSW 模块数据中心',
        operateName: '操作人',
        applyNumber: '申请编号',
        invoice: '发票',
        invoiceDate: '发票日期',
        updateStatus: '更新',
        productNumber: '产品数量',
        applyDate: '申请日期',
        rpg_group: '责任小组',
        applyStatus: '申请状态',
        accountNumber: '账号信息',
        nickName: '昵称',
        passDate: '通过时间',
        sort: '排序',
        remark: '备注',
        ctime: '创建时间',
        mtime: '更新时间',
        form: {
          operateName: '请输入操作人信息',
          applyNumber: '请输入申请编号',
          invoice: '请输入TIS Code 信息',
          productName: '请输入标准信息',
          updateStatus: '请输入更新情况',
          accountNumber: '请输入账号信息',
          invoiceDate: '请输入申请许可证',
          applyDate: '请输入申请日期',
          rpg_group: '请输入税号',
          sort: '请输入排序',
          applyStatus: '请输入申请状态',
          nickName: '请输入账号信息',
          remark: '请输入备注信息',
        },
        addNsw: '添加NSW',
        editNsw: '编辑NSW',
      },
      account: {
        title: '账号管理',
        accountNumber: '账号',
        nickname: '昵称',
        password: '密码',
        activate: '状态',
        accountMonitorList: '模块',
        feedback: '反馈',
        remark: '备注',
        ctime: '创建时间',
        mtime: '更新时间',
        form: {
          accountNumber: '请输入账号信息',
          nickname: '请输入昵称',
          password: '请输入密码',
          activate: "请选择状态",
          accountMonitorList: '请输入模块',
          feedback: '请输入反馈',
          remark: '请输入备注',
        },
        addAccount: '添加账号',
        editAccount: '编辑账号',
      }
    }
  },
  form: {
    required: '不能为空',
    userName: {
      required: '请输入用户名',
      invalid: '用户名格式不正确'
    },
    phone: {
      required: '请输入手机号',
      invalid: '手机号格式不正确'
    },
    pwd: {
      required: '请输入密码',
      invalid: '密码格式不正确，6-18位字符，包含字母、数字、下划线'
    },
    confirmPwd: {
      required: '请输入确认密码',
      invalid: '两次输入密码不一致'
    },
    code: {
      required: '请输入验证码',
      invalid: '验证码格式不正确'
    },
    email: {
      required: '请输入邮箱',
      invalid: '邮箱格式不正确'
    }
  },
  dropdown: {
    closeCurrent: '关闭',
    closeOther: '关闭其它',
    closeLeft: '关闭左侧',
    closeRight: '关闭右侧',
    closeAll: '关闭所有'
  },
  icon: {
    themeConfig: '主题配置',
    themeSchema: '主题模式',
    lang: '切换语言',
    fullscreen: '全屏',
    fullscreenExit: '退出全屏',
    reload: '刷新页面',
    collapse: '折叠菜单',
    expand: '展开菜单',
    pin: '固定',
    unpin: '取消固定'
  },
  datatable: {
    itemCount: '共 {total} 条'
  }
};

export default local;
