<script setup lang="ts">
import {$t} from '@/locales';
import {useNaiveForm} from "@/hooks/common/form";
import {translateOptions} from "@/utils/common";
import {accountDictTypeOptions, aftTypeOptions, statusTypeOptions, userGenderOptions} from "@/constants/business";

const {formRef, validate, restoreValidation} = useNaiveForm();
defineOptions({
  name: 'AccountSearch'
});

interface Emits {
  (e: 'reset'): void;

  (e: 'search'): void;
}

const emit = defineEmits<Emits>();

const model = defineModel<Api.Business.AccountParamsList>('model', {required: true});


async function reset() {
  await restoreValidation();
  emit('reset');
}

async function search() {
  await validate();
  emit('search');
}
</script>

<template>
  <NCard :title="$t('common.search')" :bordered="false" size="small" class="card-wrapper">
    <NForm ref="formRef" :model="model" label-placement="left" :label-width="100">
      <NGrid responsive="screen" item-responsive>
        <NFormItemGi span="24 s:8 m:4" :label="$t('page.business.account.accountNumber')"
                     path="accountNumber" class="pr-24px">
          <NInput v-model:value="model.accountNumber"
                  :placeholder="$t('page.business.account.form.accountNumber')"/>
        </NFormItemGi>
        <NFormItemGi span="24 s:8 m:4" :label="$t('page.business.account.nickname')" path="nickname"
                     class="pr-24px">
          <NInput v-model:value="model.nickname" :placeholder="$t('page.business.account.form.nickname')"/>
        </NFormItemGi>

        <NFormItemGi span="24 s:8 m:4" :label="$t('page.business.account.activate')" path="activate"
                     class="pr-24px">
          <NSelect
            v-model:value="model.activate"
            :placeholder="$t('page.business.account.form.activate')"
            :options="translateOptions(statusTypeOptions)"
            filterable
            clearable
          />
        </NFormItemGi>
        <NFormItemGi span="24 s:8 m:4" :label="$t('page.business.account.remark')"
                     path="applyNumber" class="pr-24px">
          <NInput v-model:value="model.remark"
                  :placeholder="$t('page.business.account.form.remark')"/>
        </NFormItemGi>
        <NFormItemGi
          span="24 s:12 m:4"
          :label="$t('page.business.account.accountMonitorList')"
          path="accountMonitorList"
          class="pr-24px"
        >
          <NSelect
            v-model:value="model.accountDictTypeOptions"
            :placeholder="$t('page.business.account.form.accountMonitorList')"
            :options="translateOptions(accountDictTypeOptions)"
            filterable
            clearable
          />
        </NFormItemGi>
        <NFormItemGi span="24 m:4" class="pr-24px">
          <NSpace class="w-full" justify="end">
            <NButton @click="reset">
              <template #icon>
                <icon-ic-round-refresh class="text-icon"/>
              </template>
              {{ $t('common.reset') }}
            </NButton>
            <NButton type="primary" ghost @click="search">
              <template #icon>
                <icon-ic-round-search class="text-icon"/>
              </template>
              {{ $t('common.search') }}
            </NButton>
          </NSpace>
        </NFormItemGi>
      </NGrid>
    </NForm>
  </NCard>
</template>

<style scoped></style>


