<script setup lang="ts">
import {$t} from '@/locales';
import {useNaiveForm} from "@/hooks/common/form";
const { formRef, validate, restoreValidation } = useNaiveForm();


defineOptions({
  name: 'CompanySearch'
});

const model = defineModel<Api.Business.LicencesListParams>('model', {required: true});

interface Emits {
  (e: 'reset'): void;
  (e: 'search'): void;
}

const emit = defineEmits<Emits>();

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
        <NFormItemGi span="24 s:8 m:5" :label="$t('page.business.license.licenseId')" path="licenseId"
                     class="pr-24px">
          <NInput v-model:value="model.licenseId" :placeholder="$t('page.business.license.form.licenseId')"/>
        </NFormItemGi>

        <NFormItemGi span="24 s:8 m:5" :label="$t('page.business.license.companyName')" path="companyName"
                     class="pr-24px">
          <NInput v-model:value="model.companyName" :placeholder="$t('page.business.license.form.companyName')"/>
        </NFormItemGi>

        <NFormItemGi span="24 s:8 m:5" :label="$t('page.business.license.taxIdentificationNumber')"
                     path="taxIdentificationNumber" class="pr-24px">
          <NInput v-model:value="model.taxIdentificationNumber"
                  :placeholder="$t('page.business.license.form.taxIdentificationNumber')"/>
        </NFormItemGi>

        <NFormItemGi span="24 s:8 m:5" :label="$t('page.business.license.issuanceTime')"
                     path="issuanceTime" class="pr-24px">
          <NInput v-model:value="model.issuanceTime"
                  :placeholder="$t('page.business.license.form.issuanceTime')"/>
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
