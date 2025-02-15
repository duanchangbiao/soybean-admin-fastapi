<script setup lang="tsx">
import {NButton, NPopconfirm} from 'naive-ui';
import {$t} from '@/locales';
import {useAppStore} from '@/store/modules/app';
import {fetchBatchDeleteLicense, fetchDeleteLicense, fetchGetLicenseList} from '@/service/api';
import {useTable, useTableOperate} from '@/hooks/common/table';
import CompanySearch from "@/views/company-info/moudules/company-search.vue";
import CompanyOperateModal from "@/views/company-info/moudules/company-operate-modal.vue";

const appStore = useAppStore();

// 获取列表信息
const {
  columns,
  columnChecks,
  data,
  getData,
  getDataByPage,
  loading,
  mobilePagination,
  resetSearchParams,
  searchParams
} = useTable({
  apiFn: fetchGetLicenseList,
  showTotal: true,
  apiParams: {
    current: 1,
    size: 10,
    licenseId: null,
    taxIdentificationNumber: null,
    companyName: null
  },
  columns: () => [
    {
      type: 'selection',
      align: 'center',
      width: 48
    },
    {
      key: 'index',
      title: $t('common.index'),
      dataIndex: 'index',
      align: 'center',
      width: 64
    },
    {
      key: 'licenseId',
      dataIndex: 'licenseId',
      title: $t('page.business.license.licenseId'),
      align: 'center',
      minWidth: 60
    },
    {
      key: 'issuanceTime',
      dataIndex: 'issuanceTime',
      title: $t('page.business.license.issuanceTime'),
      align: 'center',
      width: 100
    },
    {
      key: 'companyName',
      dataIndex: 'companyName',
      title: $t('page.business.license.companyName'),
      align: 'center',
      minWidth: 200
    },
    {
      key: 'factoryRegistrationNumber',
      dataIndex: 'factoryRegistrationNumber',
      title: $t('page.business.license.factoryRegistrationNumber'),
      align: 'center',
      width: 150
    },
    {
      key: 'taxIdentificationNumber',
      dataIndex: 'taxIdentificationNumber',
      title: $t('page.business.license.taxIdentificationNumber'),
      align: 'center',
      width: 120
    },
    {
      key: 'operate',
      title: $t('common.operate'),
      align: 'center',
      width: 130,
      // <!-- <NPopconfirm onPositiveClick={() => handleDelete(row.id)}>
      //   {{
      //     default: () => $t('common.confirmDelete'),
      //     trigger: () => (
      //       <NButton type="error" ghost size="small">
      //         {$t('common.delete')}
      //       </NButton>
      //     )
      //   }}
      // </NPopconfirm>-->
      render: row => (
        <div class="flex-center gap-8px">
          <NButton type="primary" ghost size="small" onClick={() => edit(row.id)}>
            {$t('common.edit')}
          </NButton>
        </div>
      )
    }
  ],
});

const {
  drawerVisible,
  operateType,
  handleEdit,
  handleAdd,
  checkedRowKeys,
  onBatchDeleted,
  editingData,
  onDeleted
  // closeDrawer
} = useTableOperate(data, getData);


async function handleDeleteLicense({id}: { id: number }) {
  // request
  const {error} = await fetchDeleteLicense({id});
  if (!error) {
    onDeleted();
  }
}

async function handleDelete(id: number) {
  // request
  const {error} = await handleDeleteLicense({id});
  if (!error) {
    onDeleted();
  }
}

async function handleBatchDelete() {
  // request
  const {error} = await fetchBatchDeleteLicense({ids: checkedRowKeys.value});
  if (!error) {
    onBatchDeleted();
  }
}

function edit(id: number) {
  handleEdit(id);
}
</script>

<template>
  <div class="min-h-500px flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <CompanySearch v-model:model="searchParams" @reset="resetSearchParams" @search="getData"/>
    <NCard
      :title="$t('page.business.license.title')"
      :bordered="false"
      :body-style="{ flex: 1, overflow: 'hidden' }"
      class="flex-col-stretch sm:flex-1-hidden card-wrapper"
    >
      <template #header-extra>
        <TableHeaderOperation
          v-model:columns="columnChecks"
          :disabled-delete="checkedRowKeys.length === 0"
          :loading="loading"
          table-id="license"
          @add="handleAdd"
          @delete="handleBatchDelete"
          @refresh="getData"
        />
      </template>
      <NDataTable
        v-model:checked-row-keys="checkedRowKeys"
        :columns="columns"
        :data="data"
        size="small"
        :flex-height="!appStore.isMobile"
        :scroll-x="962"
        :loading="loading"
        remote
        :row-key="row => row.id"
        :pagination="mobilePagination"
        class="sm:h-full"
      />
      <CompanyOperateModal
        v-model:visible="drawerVisible"
        :operate-type="operateType"
        :row-data="editingData"
        @submitted="getDataByPage"
      />
    </NCard>
  </div>
</template>

<style scoped></style>
