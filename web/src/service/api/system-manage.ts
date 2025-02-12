import {request} from '../request';

/** get role list */
export function fetchGetRoleList(params?: Api.SystemManage.RoleSearchParams) {
  return request<Api.SystemManage.RoleList>({
    url: '/system-manage/roles',
    method: 'get',
    params
  });
}

/** get user list */
export function fetchGetUserList(data?: Api.SystemManage.UserSearchParams) {
  return request<Api.SystemManage.UserList>({
    url: '/system-manage/users/all/',
    method: 'post',
    data
  });
}

/** get menu list */
export function fetchGetMenuList() {
  return request<Api.SystemManage.MenuList>({
    url: '/system-manage/menus',
    method: 'get'
  });
}

/** get all pages */
export function fetchGetAllPages() {
  return request<{ [key: string]: string }[]>({
    url: '/system-manage/menus/pages/',
    method: 'get'
  });
}

/** get menu tree */
export function fetchGetMenuTree() {
  return request<Api.SystemManage.MenuTree[]>({
    url: '/system-manage/menus/tree/',
    method: 'get'
  });
}

/** get menu button tree */
export function fetchGetMenuButtonTree() {
  return request<Api.SystemManage.ButtonTree[]>({
    url: '/system-manage/menus/buttons/tree/',
    method: 'get'
  });
}

/** get log list */
export function fetchGetLogList(data?: Api.SystemManage.LogSearchParams) {
  return request<Api.SystemManage.LogList>({
    url: '/system-manage/logs/all/',
    method: 'post',
    data
  });
}

/** delete log */
export function fetchDeleteLog(data?: Api.SystemManage.CommonDeleteParams) {
  return request<Api.SystemManage.LogList>({
    url: `/system-manage/logs/${data?.id}`,
    method: 'delete'
  });
}

export function fetchBatchDeleteLog(data?: Api.SystemManage.CommonBatchDeleteParams) {
  return request<Api.SystemManage.LogList>({
    url: '/system-manage/logs',
    method: 'delete',
    params: {ids: data?.ids.join(',')}
  });
}

/** update log */
export function fetchUpdateLog(data?: Api.SystemManage.LogUpdateParams) {
  return request<Api.SystemManage.LogList, 'json'>({
    url: `/system-manage/logs/${data?.id}`,
    method: 'patch',
    data
  });
}

/** get api tree */
export function fetchGetApiTree() {
  return request<Api.SystemManage.MenuTree[]>({
    url: '/system-manage/apis/tree/',
    method: 'get'
  });
}

/** refresh api from fastapi */
export function fetchRefreshAPI() {
  return request({
    url: '/system-manage/apis/refresh/',
    method: 'post'
  });
}

/** get api tags */
export function fetchGetApiTagsList() {
  return request({
    url: '/system-manage/apis/tags/all/',
    method: 'post'
  });
}

/** get api list */
export function fetchGetApiList(data?: Api.SystemManage.ApiSearchParams) {
  return request<Api.SystemManage.ApiList>({
    url: '/system-manage/apis/all/',
    method: 'post',
    data
  });
}

/** add api */
export function fetchAddApi(data?: Api.SystemManage.ApiAddParams) {
  return request<Api.SystemManage.ApiList, 'json'>({
    url: '/system-manage/apis',
    method: 'post',
    data
  });
}

/** delete api */
export function fetchDeleteApi(data?: Api.SystemManage.CommonDeleteParams) {
  return request<Api.SystemManage.ApiList>({
    url: `/system-manage/apis/${data?.id}`,
    method: 'delete'
  });
}

export function fetchBatchDeleteApi(data?: Api.SystemManage.CommonBatchDeleteParams) {
  return request<Api.SystemManage.ApiList>({
    url: '/system-manage/apis',
    method: 'delete',
    params: {ids: data?.ids.join(',')}
  });
}

/** update api */
export function fetchUpdateApi(data?: Api.SystemManage.ApiUpdateParams) {
  return request<Api.SystemManage.ApiList, 'json'>({
    url: `/system-manage/apis/${data?.id}`,
    method: 'patch',
    data
  });
}

/** add user */
export function fetchAddUser(data?: Api.SystemManage.UserUpdateParams) {
  return request<Api.SystemManage.UserList, 'json'>({
    url: '/system-manage/users',
    method: 'post',
    data
  });
}

/** update user */
export function fetchUpdateUser(data?: Api.SystemManage.UserUpdateParams) {
  return request<Api.SystemManage.UserList, 'json'>({
    url: `/system-manage/users/${data?.id}`,
    method: 'patch',
    data
  });
}

/** delete user */
export function fetchDeleteUser(data?: Api.SystemManage.CommonDeleteParams) {
  return request<Api.SystemManage.UserList>({
    url: `/system-manage/users/${data?.id}`,
    method: 'delete'
  });
}

export function fetchBatchDeleteUser(data?: Api.SystemManage.CommonBatchDeleteParams) {
  return request<Api.SystemManage.UserList>({
    url: '/system-manage/users',
    method: 'delete',
    params: {ids: data?.ids.join(',')}
  });
}

/** add role */
export function fetchAddRole(data?: Api.SystemManage.RoleUpdateParams) {
  return request<Api.SystemManage.RoleList, 'json'>({
    url: '/system-manage/roles',
    method: 'post',
    data
  });
}

/** delete role */
export function fetchDeleteRole(data?: Api.SystemManage.CommonDeleteParams) {
  return request<Api.SystemManage.RoleList>({
    url: `/system-manage/roles/${data?.id}`,
    method: 'delete'
  });
}

export function fetchBatchDeleteRole(data?: Api.SystemManage.CommonBatchDeleteParams) {
  return request<Api.SystemManage.RoleList>({
    url: '/system-manage/roles',
    method: 'delete',
    params: {ids: data?.ids.join(',')}
  });
}

/** update role */
export function fetchUpdateRole(data?: Api.SystemManage.RoleUpdateParams) {
  return request<Api.SystemManage.RoleList, 'json'>({
    url: `/system-manage/roles/${data?.id}`,
    method: 'patch',
    data
  });
}

/** get role menu ids */
export function fetchGetRoleMenu(data?: Api.SystemManage.RoleAuthorizedParams) {
  return request<Api.SystemManage.RoleAuthorizedList>({
    url: `/system-manage/roles/${data?.id}/menus`,
    method: 'get'
  });
}

/** update role menu ids */
export function fetchUpdateRoleMenu(data?: Api.SystemManage.RoleAuthorizedList) {
  return request<Api.SystemManage.RoleAuthorizedList>({
    url: `/system-manage/roles/${data?.id}/menus`,
    method: 'patch',
    data
  });
}

/** get role button ids */
export function fetchGetRoleButton(data?: Api.SystemManage.RoleAuthorizedParams) {
  return request<Api.SystemManage.RoleAuthorizedList>({
    url: `/system-manage/roles/${data?.id}/buttons`,
    method: 'get'
  });
}

/** update role button ids */
export function fetchUpdateRoleButton(data?: Api.SystemManage.RoleAuthorizedList) {
  return request<Api.SystemManage.RoleAuthorizedList>({
    url: `/system-manage/roles/${data?.id}/buttons`,
    method: 'patch',
    data
  });
}

/** get role api ids */
export function fetchGetRoleApi(data?: Api.SystemManage.RoleAuthorizedParams) {
  return request<Api.SystemManage.RoleAuthorizedList>({
    url: `/system-manage/roles/${data?.id}/apis`,
    method: 'get'
  });
}

/** update role api ids */
export function fetchUpdateRoleApi(data?: Api.SystemManage.RoleAuthorizedList) {
  return request<Api.SystemManage.RoleAuthorizedList>({
    url: `/system-manage/roles/${data?.id}/apis`,
    method: 'patch',
    data
  });
}

/** add menu */
export function fetchAddMenu(data?: Api.SystemManage.MenuAddParams) {
  return request<Api.SystemManage.MenuList, 'json'>({
    url: '/system-manage/menus',
    method: 'post',
    data
  });
}

/** delete menu */
export function fetchDeleteMenu(data?: Api.SystemManage.CommonDeleteParams) {
  return request<Api.SystemManage.MenuList>({
    url: `/system-manage/menus/${data?.id}`,
    method: 'delete'
  });
}

export function fetchBatchDeleteMenu(data?: Api.SystemManage.CommonBatchDeleteParams) {
  return request<Api.SystemManage.MenuList>({
    url: '/system-manage/menus',
    method: 'delete',
    params: {ids: data?.ids.join(',')}
  });
}

/** update menu */
export function fetchUpdateMenu(data?: Api.SystemManage.MenuUpdateParams) {
  return request<Api.SystemManage.MenuList, 'json'>({
    url: `/system-manage/menus/${data?.id}`,
    method: 'patch',
    data
  });
}


/** get license list */
export function fetchGetLicenseList(data?: Api.Business.LicencesListParams) {
  return request<Api.Business.LicencesList>({
    url: '/license/list',
    method: 'post',
    params: data
  });
}

/** delete license */
export function fetchDeleteLicense(data?: Api.SystemManage.CommonDeleteParams) {
  return request<Api.Business.LicencesList>({
    url: `/license/delete/${data?.id}`,
    method: 'delete'
  });
}


/** batch delete license */
export function fetchBatchDeleteLicense(data?: Api.SystemManage.CommonBatchDeleteParams) {
  return request<Api.Business.LicencesList>({
    url: '/license/batch',
    method: 'delete',
    params: {ids: data?.ids.join(',')}
  });
}

export function fetchAddLicense(data?: Api.Business.LicenseAddParams) {
  return request<Api.Business.LicencesList, 'json'>({
    url: '/license/add',
    method: 'post',
    data
  });
}

export function fetchUpdateLicense(data?: Api.Business.LicenseUpdateParams) {
  return request<Api.Business.LicencesList, 'json'>({
    url: `/license/update/${data?.id}`,
    method: 'patch',
    data
  });
}

/** get license */
export function fetchGetLicense(data?: Api.Business.LicencesListParams) {
  return request<Api.Business.LicencesList>({
    url: `/license/get/${data?.id}`,
    method: 'get'
  });
}

/** get aft affa list */
export function fetchGetAftList(data?: Api.Business.AftOrAffaParamsList) {
  return request<Api.Business.AftAffaList>({
    url: '/aft/list',
    method: 'post',
    params: data
  });
}

/** delete aft affa */
export function fetchDeleteAft(data?: Api.SystemManage.CommonDeleteParams) {
  return request<Api.Business.AftAffaList>({
    url: `/aft/delete/${data?.id}`,
    method: 'delete'
  });
}

/** batch delete aft affa */

export function fetchBatchDeleteAft(data?: Api.SystemManage.CommonBatchDeleteParams) {
  return request<Api.Business.AftAffaList>({
    url: '/aft/batch',
    method: 'delete',
    params: {ids: data?.ids.join(',')}
  });
}

/** add aft affa */
export function fetchAddAft(data?: Api.Business.AftOrAffaAddParams) {
  return request<Api.Business.AftAffaList, 'json'>({
    url: '/aft/add',
    method: 'post',
    data
  });
}

/** update aft affa */
export function fetchUpdateAft(data?: Api.Business.AftOrAffaUpdateParams) {
  return request<Api.Business.AftAffaList, 'json'>({
    url: `/aft/update/${data?.id}`,
    method: 'patch',
    data
  });
}

/** batch delete mor */
export function fetchBatchDeleteMor(data?: Api.SystemManage.CommonBatchDeleteParams) {
  return request<Api.Business.MorList>({
    url: '/mor/batch',
    method: 'delete',
    params: {ids: data?.ids.join(',')}
  });
}

/** get mor list */
export function fetchGetMorList(data?: Api.Business.MorParamsList) {
  return request<Api.Business.MorList>({
    url: '/mor/list',
    method: 'post',
    params: data
  });
}

/** delete mor */
export function fetchDeleteMor(data?: Api.SystemManage.CommonDeleteParams) {
  return request<Api.Business.MorList>({
    url: `/mor/delete/${data?.id}`,
    method: 'delete'
  });
}

/** add mor */
export function fetchAddMor(data?: Api.Business.MorAddParams) {
  return request<Api.Business.MorList, 'json'>({
    url: '/mor/add',
    method: 'post',
    data
  });
}

/** update mor */
export function fetchUpdateMor(data?: Api.Business.MorUpdateParams) {
  return request<Api.Business.MorList, 'json'>({
    url: `/mor/update/${data?.id}`,
    method: 'patch',
    data
  });
}

/** get mor */
export function fetchGetMor(data?: Api.Business.MorParamsList) {
  return request<Api.Business.MorList>({
    url: `/mor/get/${data?.id}`,
    method: 'get'
  });
}

/** get nsw list */
export function fetchGetNswList(data?: Api.Business.NswParamsList) {
  return request<Api.Business.NswList>({
    url: '/nsw/list',
    method: 'post',
    params: data
  });
}

/** add nsw */
export function fetchAddNsw(data?: Api.Business.NswAddParams) {
  return request<Api.Business.NswList, 'json'>({
    url: '/nsw/add',
    method: 'post',
    data
  });
}

/** get nsw */
export function fetchGetNsw(data?: Api.Business.NswParamsList) {
  return request<Api.Business.NswList>({
    url: `/nsw/get/${data?.id}`,
    method: 'get'
  });
}

/** update nsw */
export function fetchUpdateNsw(data?: Api.Business.NswUpdateParams) {
  return request<Api.Business.NswList, 'json'>({
    url: `/nsw/update/${data?.id}`,
    method: 'patch',
    data
  });
}

/** delete nsw */
export function fetchDeleteNsw(data?: Api.SystemManage.CommonDeleteParams) {
  return request<Api.Business.NswList>({
    url: `/nsw/delete/${data?.id}`,
    method: 'delete'
  });
}

/**  batch delete nsw */
export function fetchBatchDeleteNsw(data?: Api.SystemManage.CommonBatchDeleteParams) {
  return request<Api.Business.NswList>({
    url: '/nsw/batch',
    method: 'delete',
    params: {ids: data?.ids.join(',')}
  });
}

/** get account list */
export function fetchGetAccountList(data?: Api.Business.AccountParamsList) {
  return request<Api.Business.AccountList>({
    url: '/account/list',
    method: 'post',
    params: data
  });
}

/** delete account */
export function fetchDeleteAccount(data?: Api.SystemManage.CommonDeleteParams) {
  return request<Api.Business.AccountList>({
    url: `/account/delete/${data?.id}`,
    method: 'delete'
  });
}

/** batch delete account */
export function fetchBatchDeleteAccount(data?: Api.SystemManage.CommonBatchDeleteParams) {
  return request<Api.Business.AccountList>({
    url: '/account/batch',
    method: 'delete',
    params: {
      ids: data?.ids.join(',')
    }
  })
}


/** add account */
export function fetchAddAccount(data?: Api.Business.AccountAddParams) {
  return request<Api.Business.AccountList, 'json'>({
    url: '/account/add',
    method: 'post',
    data
  });
}

/** update account */
export function fetchUpdateAccount(data?: Api.Business.AccountUpdateParams) {
  return request<Api.Business.AccountList, 'json'>({
    url: `/account/update/${data?.id}`,
    method: 'patch',
    data
  });
}

/** get account */
export function fetchGetAccount(data?: Api.Business.AccountParamsList) {
  return request<Api.Business.AccountList>({
    url: `/account/get/${data?.id}`,
    method: 'get'
  });
}
