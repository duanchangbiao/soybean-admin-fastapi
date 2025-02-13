<script setup lang="ts">
import {computed, reactive, ref, watch} from "vue";
import {$t} from "@/locales";
import {fetchAddAccount, fetchGetDictList, fetchGetRoleList, fetchUpdateAccount} from "@/service/api";
import {useNaiveForm} from "@/hooks/common/form";
import {statusTypeOptions, updateStatusOptions} from "@/constants/business";
import {translateOptions} from "@/utils/common";

defineOptions({
  name: 'AccountOperateModal'
});
const visible = defineModel<boolean>('visible', {
  default: false
});

interface Emits {
  (e: 'submitted'): void;
}

interface Props {
  /** the type of operation */
  operateType: NaiveUI.TableOperateType;
  /** the edit row data */
  rowData?: Api.Business.Account | null;
}

const emit = defineEmits<Emits>();

const props = defineProps<Props>();

const model: Api.Business.AccountAddParams = reactive(createDefaultModel());

function createDefaultModel(): Api.Business.AccountAddParams {
  return {
    accountNumber: '',
    nickname: '',
    password: '',
    activate: '',
    accountMonitorList: [],
    feedback: '',
    remark: ''
  };
};


const DictOptions = ref<CommonType.Option<string>[]>([]);

async function getDictOptions() {
  const {error, data} = await fetchGetDictList({size: 1000, dictType: 'monitor', dictStatus: '1'});

  if (!error) {
    const options = data.records.map(item => ({
      label: item.dictName,
      value: item.id
    }));
    DictOptions.value = options;
  }
}

const title = computed(() => {
  const titles: Record<NaiveUI.TableOperateType, string> = {
    add: $t('page.business.account.addAccount'),
    edit: $t('page.business.account.editAccount')
  };
  return titles[props.operateType];
});

// 关闭弹框
function closeDrawer() {
  visible.value = false;
}

// 打开弹框
function handleInitModel() {
  Object.assign(model, createDefaultModel());
  if (props.operateType === 'edit' && props.rowData) {
    console.log('props.rowData', props.rowData);
    Object.assign(model, props.rowData);
  }
}

const {formRef, validate, restoreValidation} = useNaiveForm();

async function handleSubmit() {
  await validate();
  // request

  if (props.operateType === 'add') {
    const {error} = await fetchAddAccount(model);
    if (!error) {
      window.$message?.success($t('common.addSuccess'));
    }
  } else if (props.operateType === 'edit') {
    console.log(model);
    const {error} = await fetchUpdateAccount(model);
    if (!error) {
      window.$message?.success($t('common.updateSuccess'));
    }
  }

  closeDrawer();
  emit('submitted');
}

watch(visible, () => {
  if (visible.value) {
    handleInitModel();
    restoreValidation();
    getDictOptions();
  }
});
</script>

<template>
  <NModal v-model:show="visible" preset="dialog" :title="title" class="min-w-200">
    <NForm
      ref="formRef"
      :model="model"
      label-placement="left"
      label-width="auto"
      require-mark-placement="right-hanging"
      size="medium"
      class="max-w-190"
    >
      <NFormItem :label="$t('page.business.account.accountNumber')" path="accountId">
        <NInput
          v-model:value="model.accountNumber"
          :placeholder="$t('page.business.account.form.accountNumber')"
          :on-update-value="
            (value: string) => {
              model.accountNumber = value;
            }
          "
        />
      </NFormItem>
      <NFormItem :label="$t('page.business.account.nickname')" path="nickname">
        <NInput v-model:value="model.nickname" :placeholder="$t('page.business.account.form.nickname')"/>
      </NFormItem>
      <NFormItem :label="$t('page.business.account.password')" path="password">
        <NInput v-model:value="model.password" :placeholder="$t('page.business.account.form.password')"/>
      </NFormItem>
      <NFormItem :label="$t('page.business.account.activate')" path="status">
        <NSelect
          v-model:value="model.activate"
          :placeholder="$t('page.business.account.form.activate')"
          :options="translateOptions(statusTypeOptions)"
          filterable
          clearable
        />
      </NFormItem>
      <NFormItem :label="$t('page.business.account.accountMonitorList')" path="roles">
        <NSelect
          v-model:value="model.accountMonitorList"
          multiple
          filterable
          clearable
          :options="DictOptions"
          :placeholder="$t('page.business.account.form.accountMonitorList')"
        />
      </NFormItem>
      <NFormItem :label="$t('page.business.account.remark')" path="details">
        <NInput v-model:value="model.remark"
                type="textarea"
                size="small"
                :autosize="{
                  minRows: 3,
                  maxRows: 5,
                }"
                :placeholder="$t('page.business.account.form.remark')"/>
      </NFormItem>
    </NForm>
    <template #action>
      <NSpace :size="16">
        <NButton @click="closeDrawer">{{ $t('common.cancel') }}</NButton>
        <NButton type="primary" @click="handleSubmit">{{ $t('common.confirm') }}</NButton>
      </NSpace>
    </template>
  </NModal>
</template>

<style scoped>

</style>
