# PostgreSQL Database Structure

> **Host:** localhost  **Port:** 5432  **User:** postgres

## Table of Contents

- [OAuth 2](#oauth-2)
- [entity 2](#entity-2)
- [finance](#finance)
- [invoices_uat](#invoices_uat)
- [logistics 1](#logistics-1)
- [payment](#payment)
- [progressive-claim 1](#progressive-claim-1)
- [purchase](#purchase)

---

## OAuth 2

**Schemas:** authority, lite, public
**Total tables:** 73

### Schema: `authority`

#### `authority.authorization_code`

- **Type:** BASE TABLE  **Rows:** 2457

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | YES |  |  |
| `client_id` | `character varying(255)` | YES |  |  |
| `scopes` | `character varying(500)` | YES |  |  |
| `code` | `character varying(500)` | YES |  |  |
| `expiry` | `timestamp without time zone` | YES |  |  |
| `subject` | `character varying(500)` | YES |  |  |
| `redirect_uri` | `character varying(1000)` | YES |  |  |
| `nonce` | `character varying(500)` | YES |  |  |
| `code_challenge` | `character varying(255)` | YES |  |  |
| `code_challenge_method` | `character varying(255)` | YES |  |  |
| `temp_password_login` | `boolean` | YES | false |  |

#### `authority.features`

- **Type:** BASE TABLE  **Rows:** 108

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('authority.features_id_seq'::... | PK |
| `uuid` | `character varying(100)` | YES |  |  |
| `module_code` | `character varying(50)` | YES |  | FK → `authority.modules.module_code` |
| `feature_name` | `character varying(255)` | YES |  |  |
| `feature_code` | `character varying(100)` | YES |  |  |
| `category` | `character varying(255)` | YES |  |  |
| `profile` | `character varying(100)` | YES |  |  |
| `sub_category` | `character varying(100)` | YES |  |  |
| `cat_sequence` | `integer(32,0)` | YES |  |  |
| `sub_cat_sequence` | `integer(32,0)` | YES |  |  |
| `info` | `text` | YES |  |  |

**Indexes:**
- `features_feature_code_uindex`: `CREATE UNIQUE INDEX features_feature_code_uindex ON authority.features USING btree (feature_code)`
- `features_id_uindex`: `CREATE UNIQUE INDEX features_id_uindex ON authority.features USING btree (id)`
- `features_pk`: `CREATE UNIQUE INDEX features_pk ON authority.features USING btree (id)`

#### `authority.modules`

- **Type:** BASE TABLE  **Rows:** 13

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('authority.modules_id_seq'::r... | PK |
| `uuid` | `character varying(100)` | YES |  |  |
| `module_name` | `character varying(255)` | YES |  |  |
| `module_code` | `character varying(50)` | YES |  |  |
| `micro_front_end_id` | `integer(32,0)` | YES |  |  |

**Indexes:**
- `modules_id_uindex`: `CREATE UNIQUE INDEX modules_id_uindex ON authority.modules USING btree (id)`
- `modules_module_code_uindex`: `CREATE UNIQUE INDEX modules_module_code_uindex ON authority.modules USING btree (module_code)`
- `modules_pk`: `CREATE UNIQUE INDEX modules_pk ON authority.modules USING btree (id)`

#### `authority.role`

- **Type:** BASE TABLE  **Rows:** 1526

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('authority.role_id_seq'::regc... | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `name` | `character varying(1000)` | NO |  |  |
| `description` | `character varying(1000)` | YES |  |  |
| `created_by` | `character varying(255)` | YES |  |  |
| `created_at` | `timestamp with time zone` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `is_deleted` | `boolean` | YES | false |  |

**Indexes:**
- `role_id_uindex`: `CREATE UNIQUE INDEX role_id_uindex ON authority.role USING btree (id)`
- `role_pk`: `CREATE UNIQUE INDEX role_pk ON authority.role USING btree (id)`

#### `authority.role_permission`

- **Type:** BASE TABLE  **Rows:** 8183

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('authority.role_permission_id... | PK |
| `role_id` | `bigint(64,0)` | YES |  | FK → `authority.role.id` |
| `feature_id` | `bigint(64,0)` | YES |  | FK → `authority.features.id` |
| `read` | `boolean` | YES | false |  |
| `write` | `boolean` | YES | false |  |
| `approve` | `boolean` | YES | false |  |

**Indexes:**
- `role_permission_id_uindex`: `CREATE UNIQUE INDEX role_permission_id_uindex ON authority.role_permission USING btree (id)`
- `role_permission_pk`: `CREATE UNIQUE INDEX role_permission_pk ON authority.role_permission USING btree (id)`

#### `authority.subscription`

- **Type:** BASE TABLE  **Rows:** 76910

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('authority.subscription_id_se... | PK |
| `uuid` | `character varying(100)` | YES |  |  |
| `module_code` | `character varying(50)` | YES |  | FK → `authority.modules.module_code` |
| `feature_code` | `character varying(50)` | YES |  | FK → `authority.features.feature_code` |
| `start_date` | `date` | YES |  |  |
| `end_date` | `date` | YES |  |  |
| `company_uuid` | `character varying(100)` | YES |  |  |
| `feature_name` | `character varying(255)` | YES |  |  |
| `feature_id` | `bigint(64,0)` | YES |  |  |
| `fi_uuid` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |

**Indexes:**
- `subscription_id_uindex`: `CREATE UNIQUE INDEX subscription_id_uindex ON authority.subscription USING btree (id)`
- `subscription_pk`: `CREATE UNIQUE INDEX subscription_pk ON authority.subscription USING btree (id)`

#### `authority.user_privilege_action`

- **Type:** BASE TABLE  **Rows:** 91353

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('authority.user_privilege_act... | PK |
| `uuid` | `character varying(100)` | YES |  |  |
| `user_privilege_id` | `bigint(64,0)` | YES |  | FK → `authority.user_privileges.id` |
| `read` | `boolean` | YES |  |  |
| `write` | `boolean` | YES |  |  |
| `approve` | `boolean` | YES |  |  |

**Indexes:**
- `user_privilege_action_id_uindex`: `CREATE UNIQUE INDEX user_privilege_action_id_uindex ON authority.user_privilege_action USING btree (id)`
- `user_privilege_action_pk`: `CREATE UNIQUE INDEX user_privilege_action_pk ON authority.user_privilege_action USING btree (id)`

#### `authority.user_privileges`

- **Type:** BASE TABLE  **Rows:** 91353

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('authority.user_privileges_id... | PK |
| `uuid` | `character varying(100)` | YES |  |  |
| `user_uuid` | `character varying(100)` | YES |  |  |
| `feature_code` | `character varying(50)` | YES |  | FK → `authority.features.feature_code` |
| `company_uuid` | `character varying(100)` | YES |  |  |
| `privilege_action_id` | `bigint(64,0)` | YES |  | FK → `authority.user_privilege_action.id` |
| `feature_id` | `bigint(64,0)` | YES |  |  |
| `fi_uuid` | `character varying(255)` | YES |  |  |

**Indexes:**
- `user_privileges_id_uindex`: `CREATE UNIQUE INDEX user_privileges_id_uindex ON authority.user_privileges USING btree (id)`
- `user_privileges_pk`: `CREATE UNIQUE INDEX user_privileges_pk ON authority.user_privileges USING btree (id)`

### Schema: `lite`

#### `lite.plan`

- **Type:** BASE TABLE  **Rows:** 5

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('lite.plan_id_seq'::regclass) | PK |
| `plan_uuid` | `character varying(100)` | NO |  |  |
| `name` | `character varying(100)` | NO |  |  |
| `cost_in_sgd` | `double precision` | NO |  |  |
| `discount_in_percentage` | `double precision` | YES |  |  |
| `status` | `character varying(20)` | YES | 'ACTIVE'::character varying |  |
| `plan_type` | `character varying(20)` | YES |  |  |
| `description` | `text` | YES |  |  |
| `sequence` | `integer(32,0)` | YES |  |  |
| `created_on` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |
| `updated_on` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |

**Indexes:**
- `pk_plan_uuid_unique`: `CREATE UNIQUE INDEX pk_plan_uuid_unique ON lite.plan USING btree (plan_uuid)`
- `plan_name_key`: `CREATE UNIQUE INDEX plan_name_key ON lite.plan USING btree (name)`

#### `lite.plan_features`

- **Type:** BASE TABLE  **Rows:** 32

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `plan_id` | `bigint(64,0)` | NO | nextval('lite.plan_features_plan_id_s... | PK, FK → `lite.plan.id` |
| `feature_id` | `bigint(64,0)` | NO | nextval('lite.plan_features_feature_i... | PK |

#### `lite.user_plan_info`

- **Type:** BASE TABLE  **Rows:** 127

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('lite.user_plan_info_id_seq':... | PK |
| `email` | `character varying(100)` | NO |  |  |
| `user_plan_uuid` | `character varying` | NO |  |  |
| `first_name` | `character varying(100)` | NO |  |  |
| `last_name` | `character varying(100)` | YES |  |  |
| `is_entity_admin_email` | `boolean` | YES | false |  |
| `plan_id` | `bigint(64,0)` | NO | nextval('lite.user_plan_info_plan_id_... | FK → `lite.plan.id` |
| `created_on` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |
| `updated_on` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |
| `entity_uuid` | `character varying(255)` | YES |  |  |
| `status` | `boolean` | YES | true |  |
| `doxa_user_uuid` | `character varying` | YES | true |  |
| `active` | `boolean` | YES | true |  |

**Indexes:**
- `idx_user_plan_email`: `CREATE INDEX idx_user_plan_email ON lite.user_plan_info USING btree (email)`
- `idx_user_plan_uuid`: `CREATE INDEX idx_user_plan_uuid ON lite.user_plan_info USING btree (user_plan_uuid)`

#### `lite.user_plan_payment`

- **Type:** BASE TABLE  **Rows:** 121

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('lite.user_plan_payment_id_se... | PK |
| `user_plan_payment_uuid` | `character varying` | YES |  |  |
| `amount` | `double precision` | NO |  |  |
| `payment_date` | `timestamp without time zone` | YES |  |  |
| `payment_method` | `character varying(20)` | YES |  |  |
| `status` | `character varying(20)` | YES |  |  |
| `txn_id` | `character varying(255)` | YES |  |  |
| `user_plan_id` | `bigint(64,0)` | NO | nextval('lite.user_plan_payment_user_... | FK → `lite.user_plan_info.id` |
| `invoice_id` | `character varying(255)` | YES |  |  |
| `status_details` | `text` | YES |  |  |
| `doxa_entity_uuid` | `character varying(255)` | YES |  |  |
| `created_on` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |
| `updated_on` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |
| `response_invoice_id` | `character varying(255)` | YES |  |  |
| `transaction_date_time` | `timestamp without time zone` | YES |  |  |

#### `lite.user_saved_card`

- **Type:** BASE TABLE  **Rows:** 92

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('lite.user_saved_card_id_seq'... | PK |
| `user_plan_uuid` | `character varying(100)` | YES |  |  |
| `masked_card_info` | `character varying(50)` | YES |  |  |
| `exp_month_card_info` | `character varying(4)` | YES |  |  |
| `exp_year_card_info` | `character varying(10)` | YES |  |  |
| `customer_token` | `character varying` | YES |  |  |
| `name_on_card` | `character varying(150)` | YES |  |  |
| `is_active` | `boolean` | YES |  |  |
| `created_on` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |
| `updated_on` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |
| `is_primary_card` | `boolean` | YES | false |  |
| `encrypted_card_info` | `text` | YES |  |  |
| `doxa_user_uuid` | `character varying` | YES | true |  |

### Schema: `public`

#### `public.admin_categories`

- **Type:** BASE TABLE  **Rows:** 0

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('admin_categories_id_seq'::re... | PK |
| `category_name` | `character varying(50)` | NO |  |  |
| `category_code` | `character varying(50)` | NO |  |  |

#### `public.administratives`

- **Type:** BASE TABLE  **Rows:** 0

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('administratives_id_seq'::reg... | PK |
| `administrative_name` | `character varying(50)` | NO |  |  |
| `administrative_code` | `character varying(50)` | NO |  |  |
| `admin_categories_id` | `bigint(64,0)` | YES |  | FK → `public.admin_categories.id` |

#### `public.companies`

- **Type:** BASE TABLE  **Rows:** 2094

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('companies_id_seq'::regclass) | PK |
| `entity_name` | `character varying(255)` | YES |  |  |
| `gst_no` | `character varying(25)` | YES |  |  |
| `is_active` | `boolean` | YES |  |  |
| `entity_registration_no` | `character varying(255)` | NO |  |  |
| `entity_type` | `character varying(255)` | NO |  |  |
| `industry_type` | `character varying(255)` | YES |  |  |
| `is_gst_applicable` | `boolean` | YES |  |  |
| `country` | `character varying(50)` | YES |  |  |
| `onboarding_status` | `character varying(50)` | YES |  |  |
| `uuid` | `character varying(50)` | YES |  |  |
| `subscription_expiry` | `timestamp with time zone` | YES | (now() + '1 year'::interval) |  |
| `created_at` | `timestamp with time zone` | NO | now() |  |
| `updated_at` | `timestamp with time zone` | NO | now() |  |
| `entity_id` | `bigint(64,0)` | NO |  | FK → `public.entities.id` |
| `is_main` | `boolean` | YES |  |  |
| `logo_url` | `character varying(2000)` | YES |  |  |
| `buyer` | `boolean` | NO | true |  |
| `supplier` | `boolean` | NO | false |  |
| `developer` | `boolean` | NO | false |  |
| `remarks` | `character varying(1000)` | YES |  |  |
| `banner_url` | `character varying(500)` | YES |  |  |
| `video_banner_url` | `character varying(500)` | YES |  |  |
| `virtual_account_type` | `character varying(50)` | NO | 'VISA'::character varying |  |
| `is_supplier_kyc_done` | `boolean` | NO | false |  |
| `is_buyer_kyc_done` | `boolean` | NO | false |  |

**Indexes:**
- `companies_ismain_entity_index`: `CREATE INDEX companies_ismain_entity_index ON public.companies USING btree (is_main, entity_id)`
- `companies_uuid_index`: `CREATE INDEX companies_uuid_index ON public.companies USING btree (uuid)`

#### `public.company_addresses`

- **Type:** BASE TABLE  **Rows:** 262

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('company_addresses_id_seq'::r... | PK |
| `address_label` | `character varying(20)` | NO |  |  |
| `address_first_line` | `character varying(50)` | NO |  |  |
| `address_second_line` | `character varying(200)` | YES |  |  |
| `city` | `character varying(100)` | YES |  |  |
| `state` | `character varying(100)` | NO |  |  |
| `country` | `character varying(100)` | NO |  |  |
| `postal_code` | `character varying(20)` | NO |  |  |
| `uuid` | `character varying(255)` | NO |  |  |
| `country_iso_code` | `character varying(20)` | YES |  |  |
| `company_id` | `integer(32,0)` | NO |  | FK → `public.companies.id` |

**Indexes:**
- `company_addresses_company_id_key`: `CREATE UNIQUE INDEX company_addresses_company_id_key ON public.company_addresses USING btree (company_id)`

#### `public.company_categories`

- **Type:** BASE TABLE  **Rows:** 654

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('company_categories_id_seq'::... | PK |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `category_uuid` | `character varying(255)` | NO |  |  |

**Indexes:**
- `unique_company_category`: `CREATE UNIQUE INDEX unique_company_category ON public.company_categories USING btree (company_uuid, category_uuid)`

#### `public.databasechangeloglock`

- **Type:** BASE TABLE  **Rows:** 1

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO |  | PK |
| `locked` | `boolean` | NO |  |  |
| `lockgranted` | `timestamp without time zone` | YES |  |  |
| `lockedby` | `character varying(255)` | YES |  |  |

#### `public.documents_meta_data`

- **Type:** BASE TABLE  **Rows:** 18

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('documents_meta_data_id_seq':... | PK |
| `guid` | `character varying(255)` | NO |  |  |
| `title` | `character varying(255)` | NO |  |  |
| `file_name` | `character varying(255)` | NO |  |  |
| `created_at` | `timestamp with time zone` | NO | now() |  |
| `updated_at` | `timestamp with time zone` | NO | now() |  |
| `company_id` | `bigint(64,0)` | YES |  | FK → `public.companies.id` |
| `delete_from` | `bigint(64,0)` | YES |  |  |

#### `public.dtf_project`

- **Type:** BASE TABLE  **Rows:** 337

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('dtf_project_id_seq'::regclass) | PK |
| `company_name` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `project_code` | `character varying(255)` | YES |  |  |
| `project_status` | `character varying(255)` | YES |  |  |
| `project_title` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `uuid` | `character varying(255)` | YES |  |  |
| `client_id` | `character varying(255)` | YES |  |  |
| `buyer_id` | `character varying(255)` | YES |  |  |
| `proxy_pool_id` | `character varying(255)` | YES |  |  |
| `dtf_project_code` | `character varying` | YES |  |  |
| `rsid1` | `character varying(255)` | YES |  |  |
| `rsid2` | `character varying(255)` | YES |  |  |
| `cif_number` | `character varying(25)` | YES |  |  |
| `dtf_status` | `character varying(255)` | YES | 'ACTIVE'::character varying |  |
| `mt_va_gateway_lookup_id` | `bigint(64,0)` | YES |  | FK → `public.mt_va_gateway_lookup.id` |

#### `public.dtf_project_audit`

- **Type:** BASE TABLE  **Rows:** 113

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('dtf_project_audit_id_seq'::r... | PK |
| `project_uuid` | `character varying(255)` | YES |  |  |
| `action` | `character varying(255)` | YES |  |  |
| `executed_date` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |
| `project_code` | `character varying(255)` | YES |  |  |
| `project_title` | `character varying(255)` | YES |  |  |
| `company_name` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `dtf_status` | `character varying(100)` | YES |  |  |

#### `public.dtf_project_bpsp_rate`

- **Type:** BASE TABLE  **Rows:** 1049

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('dtf_project_bpsp_rate_id_seq... | PK |
| `bpsp_rate` | `double precision` | NO |  |  |
| `level` | `double precision` | NO |  |  |
| `dtf_project_id` | `bigint(64,0)` | NO |  | FK → `public.dtf_project.id` |
| `fi_id` | `bigint(64,0)` | NO |  | FK → `public.financial_institution.id` |
| `action_by_uuid` | `character varying(100)` | NO |  |  |
| `action_at` | `timestamp without time zone` | NO | now() |  |

**Indexes:**
- `dtf_project_bpsp_rate_pk`: `CREATE UNIQUE INDEX dtf_project_bpsp_rate_pk ON public.dtf_project_bpsp_rate USING btree (id)`

#### `public.dtf_project_bpsp_rate_hist`

- **Type:** BASE TABLE  **Rows:** 34440

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('dtf_project_bpsp_rate_hist_i... | PK |
| `bpsp_rate` | `double precision` | NO |  |  |
| `action_by_uuid` | `character varying(100)` | NO |  |  |
| `action_at` | `timestamp without time zone` | NO | now() |  |
| `dtf_project_bpsp_rate_id` | `bigint(64,0)` | NO |  | FK → `public.dtf_project_bpsp_rate.id` |

**Indexes:**
- `dtf_project_bpsp_rate_hist_pk`: `CREATE UNIQUE INDEX dtf_project_bpsp_rate_hist_pk ON public.dtf_project_bpsp_rate_hist USING btree (id)`

#### `public.entities`

- **Type:** BASE TABLE  **Rows:** 2049

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('entities_id_seq'::regclass) | PK |
| `entity_registration_no` | `character varying(255)` | NO |  |  |
| `uuid` | `character varying(50)` | YES |  |  |
| `entity_status` | `character varying(30)` | YES |  |  |
| `user_plan_uuid` | `character varying(50)` | YES |  |  |
| `is_doxa_lite_user` | `boolean` | YES | false |  |
| `created_on` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |
| `updated_on` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |

**Indexes:**
- `entities_entityregistrationnumber_index`: `CREATE INDEX entities_entityregistrationnumber_index ON public.entities USING btree (entity_registration_no)`
- `entities_uuid_index`: `CREATE INDEX entities_uuid_index ON public.entities USING btree (uuid)`

#### `public.entity_representative`

- **Type:** BASE TABLE  **Rows:** 5785

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('entity_representative_id_seq... | PK |
| `name` | `character varying(50)` | YES |  |  |
| `email` | `character varying(50)` | YES |  |  |
| `work_number` | `character varying(50)` | YES |  |  |
| `user_role` | `character varying(50)` | YES |  |  |
| `entity_id` | `bigint(64,0)` | YES |  | FK → `public.entities.id` |
| `country_code` | `character varying(100)` | YES |  |  |

#### `public.entity_type`

- **Type:** BASE TABLE  **Rows:** 13

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('entity_type_id_seq'::regclass) | PK |
| `entity_type` | `character varying(100)` | NO |  |  |
| `serial_number` | `character varying(50)` | YES |  |  |

**Indexes:**
- `uk_entity_type_serial_number`: `CREATE UNIQUE INDEX uk_entity_type_serial_number ON public.entity_type USING btree (serial_number)`

#### `public.fcm_notification`

- **Type:** BASE TABLE  **Rows:** 2357

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('fcm_notification_id_seq'::re... | PK |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `user_email` | `character varying(255)` | YES |  |  |
| `function_code` | `character varying(255)` | YES |  |  |
| `user_action` | `character varying(255)` | YES |  |  |
| `document_uuid` | `character varying(255)` | YES |  |  |
| `message_id` | `character varying(255)` | YES |  |  |
| `publish_fcm_token` | `character varying(255)` | YES |  |  |
| `publish_time` | `timestamp without time zone` | YES |  |  |
| `read_time` | `timestamp without time zone` | YES |  |  |
| `delete_time` | `timestamp without time zone` | YES |  |  |
| `is_deleted` | `boolean` | YES | false |  |
| `is_read` | `boolean` | YES | false |  |
| `is_successful` | `boolean` | YES | false |  |
| `message` | `character varying(255)` | YES |  |  |

#### `public.fi_company`

- **Type:** BASE TABLE  **Rows:** 173

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('fi_company_id_seq'::regclass) | PK |
| `is_active` | `boolean` | YES | false |  |
| `entity_registration_no` | `character varying(255)` | YES |  |  |
| `created_at` | `timestamp without time zone` | YES |  |  |
| `entity_name` | `character varying(255)` | YES |  |  |
| `gst_no` | `character varying(255)` | YES |  |  |
| `updated_at` | `timestamp without time zone` | YES |  |  |
| `uuid` | `character varying(255)` | YES |  |  |
| `fi_id` | `bigint(64,0)` | YES |  | FK → `public.financial_institution.id` |
| `company_status` | `character varying(255)` | YES |  |  |
| `is_supplier_financing` | `boolean` | YES | false |  |

#### `public.fi_dtf_project`

- **Type:** BASE TABLE  **Rows:** 327

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `fi_id` | `bigint(64,0)` | NO | nextval('fi_dtf_project_fi_id_seq'::r... | FK → `public.financial_institution.id` |
| `dtf_project_id` | `bigint(64,0)` | NO | nextval('fi_dtf_project_dtf_project_i... | FK → `public.dtf_project.id` |

**Indexes:**
- `unique_fi_dtf_project`: `CREATE UNIQUE INDEX unique_fi_dtf_project ON public.fi_dtf_project USING btree (fi_id, dtf_project_id)`

#### `public.fi_project`

- **Type:** BASE TABLE  **Rows:** 41

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `fi_id` | `bigint(64,0)` | NO |  | FK → `public.financial_institution.id` |
| `project_id` | `bigint(64,0)` | NO |  | FK → `public.project.id` |

**Indexes:**
- `unique_fi_project`: `CREATE UNIQUE INDEX unique_fi_project ON public.fi_project USING btree (fi_id, project_id)`

#### `public.financial_institution`

- **Type:** BASE TABLE  **Rows:** 124

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('financial_institution_id_seq... | PK |
| `fi_code` | `character varying(255)` | YES |  |  |
| `fi_name` | `character varying(255)` | YES |  |  |
| `fi_uuid` | `character varying(255)` | YES |  |  |
| `contact` | `character varying(255)` | YES |  |  |
| `country_code` | `character varying(255)` | YES |  |  |
| `designation` | `character varying(255)` | YES |  |  |
| `developer_financing` | `boolean` | YES | false |  |
| `email` | `character varying(255)` | YES |  |  |
| `fi_portal` | `boolean` | YES | false |  |
| `invoice_financing` | `boolean` | YES | false |  |
| `full_name` | `character varying(255)` | YES |  |  |
| `remarks` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `work_phone` | `character varying(255)` | YES |  |  |
| `logo_url` | `character varying(255)` | YES |  |  |
| `created_at` | `timestamp with time zone` | YES | now() |  |
| `updated_at` | `timestamp with time zone` | YES | now() |  |
| `supplier_financing` | `boolean` | YES | false |  |
| `if_term_and_condition_url` | `text` | YES |  |  |
| `sf_term_and_condition_url` | `text` | YES |  |  |
| `dtf_term_and_condition_url` | `text` | YES |  |  |
| `dtf_financing` | `boolean` | YES | false |  |

#### `public.industry_type`

- **Type:** BASE TABLE  **Rows:** 22

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('industry_type_id_seq'::regcl... | PK |
| `industry_type` | `character varying(100)` | NO |  |  |

#### `public.jsonwebtoken`

- **Type:** BASE TABLE  **Rows:** 178713

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `access_token` | `boolean` | YES |  |  |
| `expiry` | `date` | YES |  |  |
| `value` | `text` | YES |  |  |
| `revoked` | `boolean` | YES | false |  |
| `id` | `integer(32,0)` | NO | nextval('jsonwebtoken_id_seq'::regclass) | PK |

**Indexes:**
- `jsonwebtoken_id_uindex`: `CREATE UNIQUE INDEX jsonwebtoken_id_uindex ON public.jsonwebtoken USING btree (id)`
- `jsonwebtoken_pk`: `CREATE UNIQUE INDEX jsonwebtoken_pk ON public.jsonwebtoken USING btree (id)`

#### `public.language`

- **Type:** BASE TABLE  **Rows:** 1

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('language_id_seq'::regclass) | PK |
| `language_name` | `character varying(20)` | YES |  |  |
| `language_code` | `character varying(10)` | YES |  |  |

**Indexes:**
- `language_language_code_key`: `CREATE UNIQUE INDEX language_language_code_key ON public.language USING btree (language_code)`

#### `public.liquibase-changelog`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `character varying(255)` | NO |  |  |
| `author` | `character varying(255)` | NO |  |  |
| `filename` | `character varying(255)` | NO |  |  |
| `dateexecuted` | `timestamp without time zone` | NO |  |  |
| `orderexecuted` | `integer(32,0)` | NO |  |  |
| `exectype` | `character varying(10)` | NO |  |  |
| `md5sum` | `character varying(35)` | YES |  |  |
| `description` | `character varying(255)` | YES |  |  |
| `comments` | `character varying(255)` | YES |  |  |
| `tag` | `character varying(255)` | YES |  |  |
| `liquibase` | `character varying(20)` | YES |  |  |
| `contexts` | `character varying(255)` | YES |  |  |
| `labels` | `character varying(255)` | YES |  |  |
| `deployment_id` | `character varying(10)` | YES |  |  |

#### `public.liquibase-lock`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO |  | PK |
| `locked` | `boolean` | NO |  |  |
| `lockgranted` | `timestamp without time zone` | YES |  |  |
| `lockedby` | `character varying(255)` | YES |  |  |

**Indexes:**
- `LIQUIBASE-LOCK_PKEY`: `CREATE UNIQUE INDEX "LIQUIBASE-LOCK_PKEY" ON public."liquibase-lock" USING btree (id)`

#### `public.micro_front_end`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('micro_front_end_id_seq'::reg... | PK |
| `module_name` | `character varying(255)` | NO |  |  |
| `module_code` | `character varying(255)` | NO |  |  |
| `environment` | `character varying(20)` | NO |  |  |
| `host` | `character varying(500)` | NO |  |  |

**Indexes:**
- `micro_front_end_id_uindex`: `CREATE UNIQUE INDEX micro_front_end_id_uindex ON public.micro_front_end USING btree (id)`
- `micro_front_end_pk`: `CREATE UNIQUE INDEX micro_front_end_pk ON public.micro_front_end USING btree (id)`

#### `public.mt_transaction_type_lookup`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('mt_transaction_type_lookup_i... | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `rate` | `numeric(19,2)` | YES |  |  |
| `types` | `character varying(255)` | NO |  |  |

**Indexes:**
- `mt_transaction_type_lookup_uuid_key`: `CREATE UNIQUE INDEX mt_transaction_type_lookup_uuid_key ON public.mt_transaction_type_lookup USING btree (uuid)`

#### `public.mt_va_gateway_lookup`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('mt_va_gateway_lookup_id_seq'... | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `va_gateway` | `character varying(255)` | NO |  |  |

**Indexes:**
- `mt_va_gateway_lookup_uuid_key`: `CREATE UNIQUE INDEX mt_va_gateway_lookup_uuid_key ON public.mt_va_gateway_lookup USING btree (uuid)`

#### `public.opaque_token`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('opaque_token_id_seq'::regclass) | PK |
| `subject` | `text` | YES |  |  |
| `client_id` | `character varying(50)` | YES |  |  |
| `issuer` | `character varying(255)` | YES |  |  |
| `issued_at` | `date` | YES | now() |  |
| `not_before` | `date` | YES | now() |  |
| `refresh_token` | `boolean` | YES | false |  |
| `expiry` | `date` | YES |  |  |
| `value` | `text` | YES |  |  |
| `revoked` | `boolean` | YES |  |  |
| `scope` | `text` | YES |  |  |

**Indexes:**
- `opaque_token_id_uindex`: `CREATE UNIQUE INDEX opaque_token_id_uindex ON public.opaque_token USING btree (id)`
- `opaque_token_pk`: `CREATE UNIQUE INDEX opaque_token_pk ON public.opaque_token USING btree (id)`

#### `public.opaque_token_scope`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('opaque_token_scope_id_seq'::... | PK |
| `opaque_token_id` | `integer(32,0)` | NO |  |  |
| `scope` | `character varying(250)` | YES |  |  |

**Indexes:**
- `opaque_token_scope_id_uindex`: `CREATE UNIQUE INDEX opaque_token_scope_id_uindex ON public.opaque_token_scope USING btree (id)`
- `opaque_token_scope_pk`: `CREATE UNIQUE INDEX opaque_token_scope_pk ON public.opaque_token_scope USING btree (id)`

#### `public.project`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('project_id_seq'::regclass) | PK |
| `company` | `character varying(255)` | YES |  |  |
| `company_name` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `project_code` | `character varying(255)` | YES |  |  |
| `project_status` | `character varying(255)` | YES |  |  |
| `project_title` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `uuid` | `character varying(255)` | YES |  |  |

**Indexes:**
- `project_uuid_idx`: `CREATE UNIQUE INDEX project_uuid_idx ON public.project USING btree (uuid)`

#### `public.rbac_user_role`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('rbac_user_role_id_seq'::regc... | PK |
| `role_id` | `bigint(64,0)` | NO | nextval('rbac_user_role_role_id_seq':... |  |
| `user_company_id` | `bigint(64,0)` | NO | nextval('rbac_user_role_user_company_... | FK → `public.user_companies.id` |

**Indexes:**
- `rbac_user_role_id_uindex`: `CREATE UNIQUE INDEX rbac_user_role_id_uindex ON public.rbac_user_role USING btree (id)`
- `rbac_user_role_pk`: `CREATE UNIQUE INDEX rbac_user_role_pk ON public.rbac_user_role USING btree (id)`

#### `public.redirect_uris`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('redirect_uris_id_seq'::regcl... | PK |
| `identifier` | `character varying(50)` | NO |  |  |
| `client_id` | `character varying(50)` | YES |  | FK → `public.registered_client.client_id` |
| `redirect_uri` | `text` | YES |  |  |

**Indexes:**
- `client_redirect_uri_id_uindex`: `CREATE UNIQUE INDEX client_redirect_uri_id_uindex ON public.redirect_uris USING btree (id)`
- `client_redirect_uri_identifier_uindex`: `CREATE UNIQUE INDEX client_redirect_uri_identifier_uindex ON public.redirect_uris USING btree (identifier)`
- `client_redirect_uri_pk`: `CREATE UNIQUE INDEX client_redirect_uri_pk ON public.redirect_uris USING btree (id)`

#### `public.registered_client`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('registered_client_id_seq'::r... | PK |
| `identifier` | `character varying(50)` | YES |  |  |
| `client_id` | `character varying(50)` | YES |  |  |
| `client_secret` | `character varying(255)` | YES |  |  |
| `confidential` | `boolean` | YES | false |  |
| `access_token_format` | `character varying` | YES | 'jwt'::character varying |  |
| `created_at` | `date` | YES | now() |  |
| `redirect_uris` | `text` | YES |  |  |
| `cors_uris` | `text` | YES |  |  |
| `grant_types` | `character varying(255)` | YES |  |  |

**Indexes:**
- `oauth_client_client_id_index`: `CREATE INDEX oauth_client_client_id_index ON public.registered_client USING btree (client_id)`
- `oauth_client_pk`: `CREATE UNIQUE INDEX oauth_client_pk ON public.registered_client USING btree (id)`
- `oauth_client_pk_2`: `CREATE UNIQUE INDEX oauth_client_pk_2 ON public.registered_client USING btree (client_id)`

#### `public.reset_password`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('reset_password_id_seq'::regc... | PK |
| `email` | `character varying(1000)` | NO |  |  |
| `token` | `character varying(1000)` | YES |  |  |
| `expired_in` | `timestamp without time zone` | YES |  |  |
| `created_at` | `timestamp without time zone` | YES |  |  |
| `used` | `boolean` | YES | false |  |

**Indexes:**
- `reset_password_id_uindex`: `CREATE UNIQUE INDEX reset_password_id_uindex ON public.reset_password USING btree (id)`
- `reset_password_pk`: `CREATE UNIQUE INDEX reset_password_pk ON public.reset_password USING btree (id)`

#### `public.roles`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('roles_id_seq'::regclass) | PK |
| `role_name` | `character varying(25)` | NO |  |  |
| `role_code` | `character varying(25)` | NO |  |  |

#### `public.sso_domain`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('sso_domain_id_seq'::regclass) | PK |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `tenant_id` | `character varying(255)` | NO |  |  |
| `client_id` | `character varying(255)` | NO |  |  |
| `client_secret` | `character varying(255)` | NO |  |  |
| `scope` | `character varying(255)` | NO |  |  |
| `email_domain` | `character varying(50)` | NO |  |  |

**Indexes:**
- `email_domain_uindex`: `CREATE UNIQUE INDEX email_domain_uindex ON public.sso_domain USING btree (email_domain)`
- `sso_domains_pk`: `CREATE UNIQUE INDEX sso_domains_pk ON public.sso_domain USING btree (id)`

#### `public.sso_redirect_state`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('sso_redirect_state_id_seq'::... | PK |
| `state` | `character varying(255)` | NO |  |  |
| `domain_id` | `bigint(64,0)` | NO |  | FK → `public.sso_domain.id` |

**Indexes:**
- `sso_redirect_state_pk`: `CREATE UNIQUE INDEX sso_redirect_state_pk ON public.sso_redirect_state USING btree (id)`

#### `public.token`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `value` | `text` | YES |  |  |
| `expiry` | `date` | YES |  |  |
| `revoked` | `boolean` | YES |  |  |
| `accessToken` | `text` | YES |  |  |

#### `public.tradeline_platform_fee`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('tradeline_platform_fee_id_se... | PK |
| `dtf_project_id` | `bigint(64,0)` | NO |  | FK → `public.dtf_project.id` |
| `fi_id` | `bigint(64,0)` | NO |  | FK → `public.financial_institution.id` |
| `level` | `numeric` | NO |  |  |
| `platform_fee` | `numeric(19,2)` | NO | 0 |  |
| `action_by_uuid` | `character varying(255)` | NO |  |  |
| `action_at` | `timestamp without time zone` | YES |  |  |

#### `public.tradeline_platform_fee_hist`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('tradeline_platform_fee_hist_... | PK |
| `tradeline_platform_fee_id` | `bigint(64,0)` | NO |  | FK → `public.tradeline_platform_fee.id` |
| `platform_fee` | `numeric(19,2)` | NO |  |  |
| `action_by_uuid` | `character varying(255)` | NO |  |  |
| `action_at` | `timestamp without time zone` | YES |  |  |

#### `public.user_administratives`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('user_administratives_id_seq'... | PK |
| `user_companies_id` | `bigint(64,0)` | YES |  | FK → `public.user_companies.id` |
| `administratives_id` | `bigint(64,0)` | YES |  | FK → `public.administratives.id` |

#### `public.user_claim_groups`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('user_claim_groups_id_seq'::r... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `claim_group_name` | `character varying(255)` | YES |  |  |
| `claim_group_uuid` | `character varying(255)` | YES |  |  |
| `user_id` | `bigint(64,0)` | YES |  | FK → `public.users.id` |

#### `public.user_column_preference`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('user_column_preference_id_se... | PK |
| `user_uuid` | `character varying(255)` | NO |  |  |
| `screen_name` | `character varying(50)` | NO |  |  |
| `column_order` | `text` | NO |  |  |
| `created_at` | `timestamp without time zone` | NO |  |  |
| `updated_at` | `timestamp without time zone` | NO |  |  |

#### `public.user_companies`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('user_companies_id_seq'::regc... | PK |
| `user_id` | `bigint(64,0)` | YES |  | FK → `public.users.id` |
| `companies_id` | `bigint(64,0)` | YES |  | FK → `public.companies.id` |
| `user_companies_uuid` | `character varying(255)` | NO |  |  |

**Indexes:**
- `unique_user_companies`: `CREATE UNIQUE INDEX unique_user_companies ON public.user_companies USING btree (user_id, companies_id)`

#### `public.user_fcm_setting`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('user_fcm_setting_id_seq'::re... | PK |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `email` | `character varying(255)` | YES |  |  |
| `fcm_token` | `character varying(255)` | YES |  |  |
| `created_on` | `timestamp without time zone` | YES |  |  |
| `updated_on` | `timestamp without time zone` | YES |  |  |

#### `public.user_financial_institution`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('user_financial_institution_i... | PK |
| `user_financial_institution_uuid` | `character varying(255)` | YES |  |  |
| `fi_id` | `bigint(64,0)` | YES |  | FK → `public.financial_institution.id` |
| `user_id` | `bigint(64,0)` | YES |  | FK → `public.users.id` |

#### `public.user_roles`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('user_roles_id_seq'::regclass) | PK |
| `role_id` | `bigint(64,0)` | YES |  | FK → `public.roles.id` |
| `user_companies_id` | `bigint(64,0)` | YES |  | FK → `public.user_companies.id` |
| `user_financial_institution_id` | `bigint(64,0)` | YES |  | FK → `public.user_financial_institution.id` |

#### `public.user_settings`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('user_settings_id_seq'::regcl... | PK |
| `is_2fa` | `boolean` | YES | false |  |
| `language` | `bigint(64,0)` | YES |  | FK → `public.language.id` |
| `user_id` | `bigint(64,0)` | YES |  | FK → `public.users.id` |
| `two_fa_secret` | `character varying(50)` | YES |  |  |
| `must_set_password` | `boolean` | YES | false |  |

**Indexes:**
- `usersettings_user_index`: `CREATE INDEX usersettings_user_index ON public.user_settings USING btree (user_id)`

#### `public.user_temp_password_audit`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('user_temp_password_audit_id_... | PK |
| `target_user_uuid` | `character varying(255)` | YES |  |  |
| `executed_user_uuid` | `character varying(255)` | YES |  |  |
| `role` | `character varying(255)` | YES |  |  |
| `action` | `character varying(255)` | YES |  |  |
| `reason` | `character varying(255)` | YES |  |  |
| `executed_date` | `timestamp without time zone` | YES |  |  |
| `executed_user_name` | `character varying(255)` | YES |  |  |
| `password_expiry_date` | `timestamp without time zone` | YES |  |  |

#### `public.users`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('users_id_seq'::regclass) | PK |
| `email` | `character varying(50)` | NO |  |  |
| `name` | `character varying(100)` | YES |  |  |
| `password_salt` | `character varying(50)` | YES |  |  |
| `hashed_password` | `character varying(255)` | YES |  |  |
| `is_active` | `boolean` | YES | true |  |
| `is_deleted` | `boolean` | YES | true |  |
| `entity_id` | `bigint(64,0)` | YES |  | FK → `public.entities.id` |
| `created_at` | `timestamp with time zone` | NO | now() |  |
| `updated_at` | `timestamp with time zone` | NO | now() |  |
| `designation` | `character varying(255)` | YES |  |  |
| `work_number` | `character varying(255)` | YES |  |  |
| `uuid` | `character varying(255)` | NO |  |  |
| `country_code` | `character varying(50)` | YES | '65'::character varying |  |
| `remarks` | `character varying(1000)` | YES |  |  |
| `avatar_url` | `character varying(500)` | YES |  |  |
| `fi_id` | `bigint(64,0)` | YES |  | FK → `public.financial_institution.id` |
| `fi_uuid` | `character varying(255)` | YES |  |  |
| `is_new_doxa_admin_user` | `boolean` | YES | false |  |
| `user_claim_code` | `character varying(255)` | YES |  |  |
| `temporary_password` | `character varying(255)` | YES |  |  |
| `temp_pwd_expiry` | `timestamp with time zone` | YES |  |  |
| `temp_pwd_active` | `boolean` | YES |  |  |

**Indexes:**
- `users_email_uindex`: `CREATE UNIQUE INDEX users_email_uindex ON public.users USING btree (email)`
- `users_name_index`: `CREATE INDEX users_name_index ON public.users USING btree (name)`
- `users_uuid_index`: `CREATE INDEX users_uuid_index ON public.users USING btree (uuid)`

#### `public.va_evaluator_score_card`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('va_evaluator_score_card_id_s... | PK |
| `vendor_assessment_id` | `bigint(64,0)` | NO |  | FK → `public.vendor_assessment.id` |
| `evaluator_id` | `bigint(64,0)` | NO |  | FK → `public.users.id` |
| `project_id` | `bigint(64,0)` | YES |  | FK → `public.va_project.id` |
| `submission_date` | `timestamp without time zone` | YES |  |  |
| `remarks` | `text` | YES |  |  |
| `supplier` | `character varying(255)` | YES |  |  |
| `created_on` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |
| `updated_on` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |

**Indexes:**
- `idx_va_evaluator_score_card_vendor_assessment`: `CREATE INDEX idx_va_evaluator_score_card_vendor_assessment ON public.va_evaluator_score_card USING btree (vendor_assessment_id)`

#### `public.va_project`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('va_project_id_seq'::regclass) | PK |
| `vendor_assessment_id` | `bigint(64,0)` | NO |  | FK → `public.vendor_assessment.id` |
| `remarks` | `text` | YES |  |  |
| `created_on` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |
| `updated_on` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |
| `project_uuid` | `character varying(100)` | YES |  |  |

**Indexes:**
- `idx_va_project_vendor_assessment`: `CREATE INDEX idx_va_project_vendor_assessment ON public.va_project USING btree (vendor_assessment_id)`

#### `public.va_project_users`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `va_project_id` | `bigint(64,0)` | NO |  | PK, FK → `public.va_project.id` |
| `user_id` | `bigint(64,0)` | NO |  | PK, FK → `public.users.id` |

#### `public.va_score_card_parameter`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('va_score_card_parameter_id_s... | PK |
| `vendor_assessment_id` | `integer(32,0)` | NO |  | FK → `public.vendor_assessment.id` |
| `name` | `character varying(255)` | NO |  |  |
| `max_rating` | `double precision` | YES |  |  |
| `weightage_in_percentage` | `double precision` | YES |  |  |
| `description` | `text` | YES |  |  |
| `is_editable` | `boolean` | YES |  |  |
| `sequence` | `integer(32,0)` | YES |  |  |
| `created_on` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |
| `updated_on` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |
| `score_card_name` | `character varying(50)` | YES |  |  |

#### `public.va_submitted_parameter_score`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('va_submitted_parameter_score... | PK |
| `submitted_score_card_id` | `bigint(64,0)` | NO |  | FK → `public.va_evaluator_score_card.id` |
| `parameter_id` | `bigint(64,0)` | NO |  | FK → `public.va_score_card_parameter.id` |
| `system_calculated_rating` | `double precision` | YES |  |  |
| `user_rating` | `double precision` | YES |  |  |
| `evaluator_remarks` | `text` | YES |  |  |
| `created_on` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |
| `updated_on` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |

**Indexes:**
- `idx_va_submitted_parameter_score_parameter`: `CREATE INDEX idx_va_submitted_parameter_score_parameter ON public.va_submitted_parameter_score USING btree (parameter_id)`

#### `public.vendor_assessment`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('vendor_assessment_id_seq'::r... | PK |
| `title` | `character varying(255)` | NO |  |  |
| `type` | `character varying(50)` | YES |  |  |
| `period_from` | `date` | YES |  |  |
| `period_to` | `date` | YES |  |  |
| `evaluation_from` | `date` | YES |  |  |
| `evaluation_to` | `date` | YES |  |  |
| `remarks` | `text` | YES |  |  |
| `status` | `character varying(50)` | YES |  |  |
| `company_uuid` | `character varying(100)` | YES |  |  |
| `created_by_id` | `bigint(64,0)` | NO |  | FK → `public.users.id` |
| `app_status` | `character varying(50)` | YES | 'ACTIVE'::character varying |  |
| `created_on` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |
| `updated_on` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |

**Indexes:**
- `idx_vendor_assessment_status`: `CREATE INDEX idx_vendor_assessment_status ON public.vendor_assessment USING btree (status)`
- `idx_vendor_assessment_type`: `CREATE INDEX idx_vendor_assessment_type ON public.vendor_assessment USING btree (type)`

#### `public.virtual_card_dtf_fee`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('virtual_card_dtf_fee_id_seq'... | PK |
| `dtf_project_id` | `bigint(64,0)` | NO |  | FK → `public.dtf_project.id` |
| `fi_id` | `bigint(64,0)` | NO |  | FK → `public.financial_institution.id` |
| `level` | `numeric` | NO |  |  |
| `mt_transaction_type_lookup_id` | `bigint(64,0)` | YES |  | FK → `public.mt_transaction_type_lookup.id` |
| `action_by_uuid` | `character varying(255)` | NO |  |  |
| `action_at` | `timestamp without time zone` | YES |  |  |

#### `public.virtual_card_dtf_fee_hist`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('virtual_card_dtf_fee_hist_id... | PK |
| `virtual_card_dtf_fee_id` | `bigint(64,0)` | NO |  | FK → `public.virtual_card_dtf_fee.id` |
| `mt_transaction_type_lookup_id` | `bigint(64,0)` | YES |  | FK → `public.mt_transaction_type_lookup.id` |
| `rate` | `numeric(19,2)` | YES |  |  |
| `types` | `character varying(255)` | YES |  |  |
| `action_by_uuid` | `character varying(255)` | NO |  |  |
| `action_at` | `timestamp without time zone` | YES |  |  |

#### `public.virtual_card_platform_fee`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('virtual_card_platform_fee_id... | PK |
| `dtf_project_id` | `bigint(64,0)` | NO |  | FK → `public.dtf_project.id` |
| `fi_id` | `bigint(64,0)` | NO |  | FK → `public.financial_institution.id` |
| `level` | `numeric` | NO |  |  |
| `platform_fee` | `numeric(19,2)` | NO | 0 |  |
| `action_by_uuid` | `character varying(255)` | NO |  |  |
| `action_at` | `timestamp without time zone` | YES |  |  |

#### `public.virtual_card_platform_fee_hist`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('virtual_card_platform_fee_hi... | PK |
| `virtual_card_platform_fee_id` | `bigint(64,0)` | NO |  | FK → `public.virtual_card_platform_fee.id` |
| `platform_fee` | `numeric(19,2)` | NO |  |  |
| `action_by_uuid` | `character varying(255)` | NO |  |  |
| `action_at` | `timestamp without time zone` | YES |  |  |

---

## entity 2

**Schemas:** public
**Total tables:** 95

### Schema: `public`

#### `public.addresses`

- **Type:** BASE TABLE  **Rows:** 7364

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('addresses_id_seq'::regclass) | PK |
| `address_label` | `character varying(100)` | NO |  |  |
| `address_first_line` | `character varying(500)` | NO |  |  |
| `address_second_line` | `character varying(200)` | YES |  |  |
| `city` | `character varying(100)` | YES |  |  |
| `state` | `character varying(100)` | NO |  |  |
| `country` | `character varying(100)` | NO |  |  |
| `postal_code` | `character varying(20)` | NO |  |  |
| `uuid` | `character varying(255)` | NO |  |  |
| `is_default` | `boolean` | NO |  |  |
| `is_active` | `boolean` | NO |  |  |
| `company_uuid` | `character varying(100)` | YES |  |  |
| `vendor_id` | `bigint(64,0)` | YES |  | FK → `public.vendors.id` |
| `supplier_id` | `bigint(64,0)` | YES |  | FK → `public.suppliers.id` |
| `created_on` | `timestamp with time zone` | YES | now() |  |
| `updated_on` | `timestamp with time zone` | YES | now() |  |
| `country_iso_code` | `character varying(20)` | YES |  |  |
| `is_deleted` | `boolean` | NO | false |  |
| `is_used` | `boolean` | NO | false |  |
| `is_archived` | `boolean` | YES | false |  |

**Indexes:**
- `address_first_line_index`: `CREATE INDEX address_first_line_index ON public.addresses USING btree (address_first_line)`
- `address_label_index`: `CREATE INDEX address_label_index ON public.addresses USING btree (address_label)`
- `country_index`: `CREATE INDEX country_index ON public.addresses USING btree (country)`
- `postal_code_index`: `CREATE INDEX postal_code_index ON public.addresses USING btree (postal_code)`
- `state_index`: `CREATE INDEX state_index ON public.addresses USING btree (state)`
- `uuid_index`: `CREATE INDEX uuid_index ON public.addresses USING btree (uuid)`

#### `public.ap_specialist`

- **Type:** BASE TABLE  **Rows:** 225

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('ap_specialist_id_seq'::regcl... | PK |
| `uuid` | `character varying(50)` | YES |  |  |
| `company_uuid` | `character varying(50)` | YES |  |  |
| `group_code` | `character varying(255)` | YES |  |  |
| `updated_on` | `timestamp with time zone` | YES | now() |  |
| `updated_by_uuid` | `character varying(50)` | YES |  |  |
| `updated_by_name` | `character varying(255)` | YES |  |  |
| `created_on` | `timestamp with time zone` | YES | now() |  |
| `created_by_uuid` | `character varying(50)` | YES |  |  |
| `created_by_name` | `character varying(255)` | YES |  |  |
| `remarks` | `character varying(500)` | YES |  |  |

#### `public.ap_specialist_users`

- **Type:** BASE TABLE  **Rows:** 441

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('ap_specialist_users_id_seq':... | PK |
| `user_uuid` | `character varying(50)` | YES |  |  |
| `user_name` | `character varying(255)` | YES |  |  |
| `ap_specialist_id` | `bigint(64,0)` | YES |  | FK → `public.ap_specialist.id` |

#### `public.approval_configuration`

- **Type:** BASE TABLE  **Rows:** 28142

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('approval_configuration_id_se... | PK |
| `feature_code` | `character varying(100)` | NO |  |  |
| `feature_name` | `character varying(100)` | NO |  |  |
| `approval_features_id` | `bigint(64,0)` | YES |  | FK → `public.approval_features.id` |
| `is_optional` | `boolean` | YES | true |  |
| `company_uuid` | `character varying(100)` | YES |  |  |
| `created_by_uuid` | `character varying(100)` | YES |  |  |
| `created_by_name` | `character varying(100)` | YES |  |  |
| `created_on` | `timestamp with time zone` | NO | now() |  |

#### `public.approval_features`

- **Type:** BASE TABLE  **Rows:** 31

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('approval_features_id_seq'::r... | PK |
| `feature_code` | `character varying(255)` | NO |  |  |
| `feature_name` | `character varying(255)` | NO |  |  |
| `created_by_uuid` | `character varying(100)` | YES |  |  |
| `created_by_name` | `character varying(100)` | YES |  |  |
| `created_on` | `timestamp with time zone` | NO | now() |  |
| `is_used` | `boolean` | YES | false |  |
| `uuid` | `character varying(255)` | NO |  |  |
| `is_active` | `boolean` | YES | true |  |

#### `public.approval_group`

- **Type:** BASE TABLE  **Rows:** 2738

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('approval_group_id_seq'::regc... | PK |
| `approval_range_id` | `bigint(64,0)` | YES |  | FK → `public.approval_range.id` |
| `group_id` | `bigint(64,0)` | YES |  | FK → `public.groups.id` |
| `sequence` | `integer(32,0)` | NO |  |  |
| `number_approvers` | `integer(32,0)` | NO |  |  |

**Indexes:**
- `approval_group_approval_range_id_idx`: `CREATE INDEX approval_group_approval_range_id_idx ON public.approval_group USING btree (approval_range_id)`

#### `public.approval_matrix`

- **Type:** BASE TABLE  **Rows:** 2054

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('approval_matrix_id_seq'::reg... | PK |
| `approval_code` | `character varying(25)` | NO |  |  |
| `approval_name` | `character varying(200)` | NO |  |  |
| `task_management_id` | `bigint(64,0)` | YES |  | FK → `public.task_management.id` |
| `created_by_uuid` | `character varying(100)` | YES |  |  |
| `company_uuid` | `character varying(100)` | YES |  |  |
| `created_on` | `timestamp with time zone` | NO | now() |  |
| `is_active` | `boolean` | YES | true |  |
| `uuid` | `character varying(255)` | NO |  |  |
| `created_by_name` | `character varying(100)` | YES |  |  |
| `task_code` | `character varying(50)` | YES |  |  |
| `task_name` | `character varying(255)` | YES |  |  |
| `approval_features_id` | `bigint(64,0)` | YES |  |  |

**Indexes:**
- `approval_matrix_uuid_index`: `CREATE INDEX approval_matrix_uuid_index ON public.approval_matrix USING btree (uuid)`

#### `public.approval_matrix_audit_trail`

- **Type:** BASE TABLE  **Rows:** 1879

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('approval_matrix_audit_trail_... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `action` | `character varying(255)` | YES |  |  |
| `date_time` | `timestamp with time zone` | NO | now() |  |
| `approval_matrix_id` | `bigint(64,0)` | YES |  | FK → `public.approval_matrix.id` |

#### `public.approval_matrix_in_use`

- **Type:** BASE TABLE  **Rows:** 2435

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('approval_matrix_in_use_id_se... | PK |
| `approval_matrix_uuid` | `character varying(255)` | NO |  |  |
| `feature_uuid` | `character varying(255)` | NO |  |  |
| `feature_number` | `character varying(255)` | YES |  |  |
| `feature_type` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `requester_uuid` | `character varying(255)` | NO |  |  |
| `requester_name` | `character varying(255)` | NO |  |  |
| `created_at` | `timestamp with time zone` | NO | now() |  |
| `total_amount` | `double precision` | YES |  |  |
| `currency_code` | `character varying(50)` | YES |  |  |

#### `public.approval_matrix_project`

- **Type:** BASE TABLE  **Rows:** 434

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('approval_matrix_project_id_s... | PK |
| `project_uuid` | `character varying(255)` | YES |  |  |
| `project_code` | `character varying(255)` | YES |  |  |
| `project_name` | `character varying(255)` | YES |  |  |
| `project_id` | `bigint(64,0)` | YES |  | FK → `public.projects.id` |
| `approval_matrix_id` | `bigint(64,0)` | YES |  | FK → `public.approval_matrix.id` |
| `approval_matrix_uuid` | `character varying(255)` | YES |  |  |

#### `public.approval_range`

- **Type:** BASE TABLE  **Rows:** 2373

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('approval_range_id_seq'::regc... | PK |
| `is_value_criteria` | `character varying(25)` | NO |  |  |
| `range_from` | `double precision` | NO |  |  |
| `range_to` | `double precision` | NO |  |  |
| `approval_matrix_id` | `bigint(64,0)` | YES |  | FK → `public.approval_matrix.id` |

**Indexes:**
- `approval_range_approval_matrix_id_idx`: `CREATE INDEX approval_range_approval_matrix_id_idx ON public.approval_range USING btree (approval_matrix_id)`

#### `public.bank_account`

- **Type:** BASE TABLE  **Rows:** 470

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('bank_account_id_seq'::regclass) | PK |
| `uuid` | `character varying(50)` | YES |  |  |
| `company_uuid` | `character varying(50)` | YES |  |  |
| `bank_label` | `character varying(255)` | YES |  |  |
| `country` | `character varying(255)` | YES |  |  |
| `bank_name` | `character varying(255)` | YES |  |  |
| `bank_account_no` | `character varying(255)` | YES |  |  |
| `account_holder_name` | `character varying(255)` | YES |  |  |
| `currency` | `character varying(255)` | YES |  |  |
| `swift_code` | `character varying(50)` | YES |  |  |
| `branch` | `character varying(255)` | YES |  |  |
| `branch_code` | `character varying(50)` | YES |  |  |
| `branch_city` | `character varying(255)` | YES |  |  |
| `branch_address_line1` | `character varying(255)` | YES |  |  |
| `branch_address_line2` | `character varying(255)` | YES |  |  |
| `postal_code` | `character varying(50)` | YES |  |  |
| `state_province` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `requestor_uuid` | `character varying(50)` | YES |  |  |
| `requestor_name` | `character varying(255)` | YES |  |  |
| `approver_uuid` | `character varying(50)` | YES |  |  |
| `approver_name` | `character varying(255)` | YES |  |  |
| `updated_on` | `timestamp with time zone` | YES | now() |  |
| `approved_date` | `timestamp with time zone` | YES |  |  |
| `default_account` | `boolean` | YES |  |  |
| `default_account_before_approval` | `boolean` | YES |  |  |
| `original_account_uuid` | `character varying(255)` | YES |  |  |
| `is_active` | `boolean` | YES | true |  |

**Indexes:**
- `bank_account_companyuuid_index`: `CREATE INDEX bank_account_companyuuid_index ON public.bank_account USING btree (company_uuid)`
- `bank_account_companyuuid_labelaccnoaccountholdername_index`: `CREATE INDEX bank_account_companyuuid_labelaccnoaccountholdername_index ON public.bank_account USING btree (company_uuid, bank_label, bank_account_no, account_holder_name)`
- `bank_account_companyuuid_uuid_index`: `CREATE INDEX bank_account_companyuuid_uuid_index ON public.bank_account USING btree (company_uuid, uuid)`

#### `public.bank_account_audit_trail`

- **Type:** BASE TABLE  **Rows:** 843

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('bank_account_audit_trail_id_... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(50)` | YES |  |  |
| `action` | `character varying(100)` | YES |  |  |
| `date_time` | `timestamp with time zone` | NO | now() |  |
| `approval_group` | `character varying(100)` | YES |  |  |
| `bank_account_id` | `bigint(64,0)` | YES |  | FK → `public.bank_account.id` |

#### `public.bank_account_document_metadata`

- **Type:** BASE TABLE  **Rows:** 1

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('bank_account_document_metada... | PK |
| `guid` | `character varying(50)` | YES |  |  |
| `file_label` | `character varying(50)` | YES |  |  |
| `file_description` | `character varying(255)` | YES |  |  |
| `uploaded_on` | `timestamp with time zone` | NO | now() |  |
| `uploaded_by` | `character varying(100)` | YES |  |  |
| `uploader_uuid` | `character varying(50)` | YES |  |  |
| `external_document` | `boolean` | YES |  |  |
| `bank_account_id` | `bigint(64,0)` | YES |  | FK → `public.bank_account.id` |

#### `public.bank_info`

- **Type:** BASE TABLE  **Rows:** 112799

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('bank_info_id_seq'::regclass) | PK |
| `bank_name` | `character varying(255)` | YES |  |  |
| `branch` | `character varying(255)` | YES |  |  |
| `city` | `character varying(50)` | YES |  |  |
| `swift_code` | `character varying(255)` | YES |  |  |
| `iso_country_currency_id` | `bigint(64,0)` | YES |  | FK → `public.isocountry_currency.id` |

#### `public.catalogue_item_project`

- **Type:** BASE TABLE  **Rows:** 805

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('catalogue_item_project_id_se... | PK |
| `item_id` | `bigint(64,0)` | NO |  | FK → `public.catalogues.id` |
| `project_id` | `bigint(64,0)` | NO |  | FK → `public.projects.id` |

**Indexes:**
- `catalogue_item_project_id_uindex`: `CREATE UNIQUE INDEX catalogue_item_project_id_uindex ON public.catalogue_item_project USING btree (id)`

#### `public.catalogues`

- **Type:** BASE TABLE  **Rows:** 78534

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('catalogues_id_seq'::regclass) | PK |
| `item_code` | `character varying(100)` | NO |  |  |
| `item_name` | `character varying(200)` | NO |  |  |
| `uom_code` | `character varying(20)` | NO |  |  |
| `supplier_id` | `bigint(64,0)` | YES |  | FK → `public.suppliers.id` |
| `supplier_code` | `character varying(255)` | YES |  |  |
| `supplier_name` | `character varying(255)` | YES |  |  |
| `tax_code` | `character varying(50)` | YES |  |  |
| `tax_rate` | `double precision` | YES |  |  |
| `currency_code` | `character varying(50)` | YES |  |  |
| `unit_price` | `double precision` | YES |  |  |
| `valid_from` | `date` | YES |  |  |
| `valid_to` | `date` | YES |  |  |
| `description` | `character varying(500)` | YES |  |  |
| `updated_on` | `timestamp without time zone` | YES |  |  |
| `is_active` | `boolean` | YES | true |  |
| `company_uuid` | `character varying(100)` | NO |  |  |
| `item_model` | `character varying(200)` | YES |  |  |
| `item_size` | `character varying(200)` | YES |  |  |
| `item_brand` | `character varying(200)` | YES |  |  |
| `item_type` | `character varying(30)` | YES |  |  |
| `item_category` | `character varying(100)` | YES |  |  |
| `item_material` | `character varying(50)` | YES |  |  |
| `uuid` | `character varying(100)` | YES |  |  |
| `created_on` | `timestamp without time zone` | YES |  |  |
| `gl_account_number` | `character varying(20)` | YES |  |  |
| `trade_code` | `character varying(20)` | YES |  |  |
| `category_id` | `bigint(64,0)` | YES |  | FK → `public.category.id` |
| `is_manual` | `boolean` | YES | false |  |
| `supplier_uuid` | `character varying(255)` | YES |  |  |
| `remain_draw_down_qty` | `double precision` | YES | 0 |  |
| `contracted` | `boolean` | YES | false |  |
| `contracted_qty` | `double precision` | YES | 0 |  |
| `contracted_price` | `double precision` | YES | 0 |  |
| `contracted_ref_no` | `character varying(200)` | YES |  |  |
| `is_deleted` | `boolean` | NO | false |  |
| `is_used` | `boolean` | NO | false |  |
| `unit_price_str` | `character varying(255)` | YES |  |  |
| `contracted_qty_str` | `character varying(255)` | YES |  |  |
| `contracted_price_str` | `character varying(255)` | YES |  |  |
| `tax_id` | `bigint(64,0)` | YES |  | FK → `public.taxes.id` |
| `uom_id` | `bigint(64,0)` | YES |  | FK → `public.uom.id` |
| `trade_id` | `bigint(64,0)` | YES |  | FK → `public.trades.id` |
| `image_url` | `character varying` | YES |  |  |
| `hs_code` | `character varying(255)` | YES |  |  |

**Indexes:**
- `catalogue_company_index`: `CREATE INDEX catalogue_company_index ON public.catalogues USING btree (company_uuid)`
- `catalogue_company_item_index`: `CREATE INDEX catalogue_company_item_index ON public.catalogues USING btree (item_code, company_uuid)`

#### `public.category`

- **Type:** BASE TABLE  **Rows:** 12702

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('category_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `category_name` | `character varying(100)` | NO |  |  |
| `category_description` | `character varying(255)` | YES |  |  |
| `action` | `character varying(20)` | YES |  |  |
| `updated_on` | `timestamp without time zone` | YES |  |  |
| `updated_by` | `character varying(255)` | YES |  |  |
| `is_active` | `boolean` | YES | true |  |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `created_on` | `timestamp without time zone` | YES |  |  |
| `created_by` | `character varying(255)` | YES |  |  |
| `is_deleted` | `boolean` | NO | false |  |
| `parent_id` | `bigint(64,0)` | YES |  | FK → `public.modules.id` |
| `sale_id` | `bigint(64,0)` | YES |  |  |
| `category_type` | `character varying(50)` | YES |  |  |
| `is_used` | `boolean` | NO | false |  |
| `path` | `character varying(500)` | YES |  |  |
| `serial_number` | `character varying(50)` | YES |  |  |

**Indexes:**
- `category_category_name_index`: `CREATE INDEX category_category_name_index ON public.category USING btree (category_name)`
- `category_company_index`: `CREATE INDEX category_company_index ON public.category USING btree (company_uuid)`
- `category_uuid_index`: `CREATE INDEX category_uuid_index ON public.category USING btree (uuid)`
- `uk_category_serial_company`: `CREATE UNIQUE INDEX uk_category_serial_company ON public.category USING btree (serial_number, company_uuid)`

#### `public.claim_category`

- **Type:** BASE TABLE  **Rows:** 104

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('claim_category_id_seq'::regc... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `name` | `character varying(255)` | YES |  |  |
| `description` | `text` | YES |  |  |
| `is_active` | `boolean` | YES |  |  |
| `is_deleted` | `boolean` | YES | false |  |
| `is_used` | `boolean` | YES | false |  |
| `created_on` | `timestamp with time zone` | NO | now() |  |
| `updated_on` | `timestamp with time zone` | NO | now() |  |

#### `public.claim_group`

- **Type:** BASE TABLE  **Rows:** 59

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('claim_group_id_seq'::regclass) | PK |
| `uuid` | `character varying(50)` | YES |  |  |
| `company_uuid` | `character varying(50)` | YES |  |  |
| `group_name` | `character varying(255)` | YES |  |  |
| `no_of_creator` | `integer(32,0)` | YES | 0 |  |
| `created_by` | `character varying(255)` | YES |  |  |
| `remarks` | `text` | YES |  |  |
| `is_active` | `boolean` | YES |  |  |
| `is_used` | `boolean` | YES | false |  |
| `created_on` | `timestamp without time zone` | YES | now() |  |
| `updated_on` | `timestamp without time zone` | YES |  |  |

#### `public.claim_group_creator`

- **Type:** BASE TABLE  **Rows:** 134

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('claim_group_creator_id_seq':... | PK |
| `uuid` | `character varying(50)` | YES |  |  |
| `creator_name` | `character varying(255)` | YES |  |  |
| `creator_uuid` | `character varying(50)` | YES |  |  |
| `claim_group_id` | `bigint(64,0)` | NO |  | FK → `public.claim_group.id` |

#### `public.company_category`

- **Type:** BASE TABLE  **Rows:** 42

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('company_category_id_seq'::re... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `code` | `character varying(255)` | YES |  |  |
| `name` | `character varying(255)` | YES |  |  |
| `description` | `text` | YES |  |  |
| `is_active` | `boolean` | YES |  |  |
| `created_on` | `timestamp with time zone` | NO | now() |  |
| `updated_on` | `timestamp with time zone` | NO | now() |  |

**Indexes:**
- `unique_company_code`: `CREATE UNIQUE INDEX unique_company_code ON public.company_category USING btree (company_uuid, code)`

#### `public.company_tier`

- **Type:** BASE TABLE  **Rows:** 18

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('company_tier_id_seq'::regclass) |  |
| `tier_id` | `bigint(64,0)` | YES |  | FK → `public.tiers.id` |
| `supplier_id` | `bigint(64,0)` | YES |  | FK → `public.suppliers.id` |

#### `public.connection_requester`

- **Type:** BASE TABLE  **Rows:** 869

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('connection_requester_id_seq'... | PK |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `entity_name` | `character varying(255)` | YES |  |  |
| `gst_no` | `character varying(255)` | YES |  |  |
| `is_gst_applicable` | `boolean` | YES |  |  |
| `company_registration_number` | `character varying(255)` | YES |  |  |
| `country` | `character varying(255)` | YES |  |  |

#### `public.connections`

- **Type:** BASE TABLE  **Rows:** 1233

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('connections_id_seq'::regclass) | PK |
| `created_on` | `timestamp with time zone` | NO | now() |  |
| `is_deleted` | `boolean` | YES | false |  |
| `updated_on` | `timestamp with time zone` | NO | now() |  |
| `reason` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | NO |  |  |
| `created_by_user_uuid` | `character varying(255)` | YES |  |  |
| `updated_by_user_uuid` | `character varying(255)` | YES |  |  |
| `requested_by_company_uuid` | `character varying(255)` | YES |  |  |
| `requested_to_supplier_id` | `bigint(64,0)` | YES |  | FK → `public.suppliers.id` |
| `token` | `character varying(255)` | YES |  |  |
| `responded_by_user_uuid` | `character varying(255)` | YES |  |  |
| `is_active` | `boolean` | YES |  |  |
| `last_disconnected_date` | `timestamp with time zone` | YES |  |  |
| `uuid` | `character varying(255)` | NO |  |  |
| `connection_requester_id` | `bigint(64,0)` | YES |  | FK → `public.connection_requester.id` |

**Indexes:**
- `connection_uuid_index`: `CREATE INDEX connection_uuid_index ON public.connections USING btree (uuid)`
- `requested_by_id_index`: `CREATE INDEX requested_by_id_index ON public.connections USING btree (requested_by_company_uuid)`
- `requested_to_id_index`: `CREATE INDEX requested_to_id_index ON public.connections USING btree (requested_to_supplier_id)`
- `responded_by_id_index`: `CREATE INDEX responded_by_id_index ON public.connections USING btree (responded_by_user_uuid)`
- `status_index`: `CREATE INDEX status_index ON public.connections USING btree (status)`
- `token_index`: `CREATE INDEX token_index ON public.connections USING btree (token)`

#### `public.cost_code`

- **Type:** BASE TABLE  **Rows:** 43473

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('cost_code_id_seq'::regclass) | PK |
| `code` | `character varying(255)` | YES |  |  |
| `remark` | `character varying(255)` | YES |  |  |
| `gl_id` | `bigint(64,0)` | YES |  | FK → `public.general_ledger.id` |

**Indexes:**
- `cost_code_gl_id_index`: `CREATE INDEX cost_code_gl_id_index ON public.cost_code USING btree (gl_id)`

#### `public.credit_facility`

- **Type:** BASE TABLE  **Rows:** 361

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('credit_facility_id_seq'::reg... | PK |
| `uuid` | `character varying(100)` | NO |  |  |
| `fi_uuid` | `character varying(100)` | NO |  |  |
| `dtf_project_uuid` | `character varying(100)` | NO |  |  |
| `company_uuid` | `character varying(100)` | NO |  |  |
| `status` | `character varying(100)` | NO |  |  |
| `issue_vc` | `boolean` | NO | false |  |

**Indexes:**
- `credit_facility_pk`: `CREATE UNIQUE INDEX credit_facility_pk ON public.credit_facility USING btree (id)`

#### `public.currencies`

- **Type:** BASE TABLE  **Rows:** 296587

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('currencies_id_seq'::regclass) | PK |
| `currency_code` | `character varying(50)` | NO |  |  |
| `currency_name` | `character varying(50)` | NO |  |  |
| `is_active` | `boolean` | YES | false |  |
| `is_default` | `boolean` | YES |  |  |
| `exchange_rate` | `double precision` | NO |  |  |
| `company_uuid` | `character varying(100)` | NO |  |  |
| `uuid` | `character varying(100)` | YES |  |  |
| `created_on` | `timestamp with time zone` | YES | now() |  |
| `updated_on` | `timestamp with time zone` | YES | now() |  |

**Indexes:**
- `currencies_company_currencycode_index`: `CREATE INDEX currencies_company_currencycode_index ON public.currencies USING btree (company_uuid, currency_code)`
- `currencies_company_index`: `CREATE INDEX currencies_company_index ON public.currencies USING btree (company_uuid)`
- `currencies_company_isdefault_index`: `CREATE INDEX currencies_company_isdefault_index ON public.currencies USING btree (company_uuid, is_default)`

#### `public.databasechangeloglock`

- **Type:** BASE TABLE  **Rows:** 1

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO |  | PK |
| `locked` | `boolean` | NO |  |  |
| `lockgranted` | `timestamp without time zone` | YES |  |  |
| `lockedby` | `character varying(255)` | YES |  |  |

#### `public.default_payment_terms`

- **Type:** BASE TABLE  **Rows:** 12

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('default_payment_terms_id_seq... | PK |
| `name` | `character varying(1000)` | YES |  |  |
| `pt_day` | `integer(32,0)` | NO |  |  |
| `remarks` | `character varying(1000)` | YES |  |  |

**Indexes:**
- `default_payment_terms_id_uindex`: `CREATE UNIQUE INDEX default_payment_terms_id_uindex ON public.default_payment_terms USING btree (id)`
- `default_payment_terms_pk`: `CREATE UNIQUE INDEX default_payment_terms_pk ON public.default_payment_terms USING btree (id)`

#### `public.department_code`

- **Type:** BASE TABLE  **Rows:** 26965

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('department_code_id_seq'::reg... | PK |
| `code` | `character varying(255)` | YES |  |  |
| `remark` | `character varying(255)` | YES |  |  |
| `gl_id` | `bigint(64,0)` | YES |  | FK → `public.general_ledger.id` |

**Indexes:**
- `department_code_gl_id_index`: `CREATE INDEX department_code_gl_id_index ON public.department_code USING btree (gl_id)`

#### `public.document_template`

- **Type:** BASE TABLE  **Rows:** 50

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('document_template_id_seq'::r... | PK |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `po_w_price` | `character varying(255)` | YES |  |  |
| `po_wo_price` | `character varying(255)` | YES |  |  |

**Indexes:**
- `unique_company_uuid`: `CREATE UNIQUE INDEX unique_company_uuid ON public.document_template USING btree (company_uuid)`

#### `public.documents_meta_data`

- **Type:** BASE TABLE  **Rows:** 0

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('documents_meta_data_id_seq':... | PK |
| `guid` | `character varying(255)` | NO |  |  |
| `title` | `character varying(255)` | NO |  |  |
| `file_name` | `character varying(255)` | NO |  |  |
| `created_at` | `timestamp with time zone` | NO | now() |  |
| `updated_at` | `timestamp with time zone` | NO | now() |  |
| `company_id` | `bigint(64,0)` | YES |  |  |
| `delete_from` | `bigint(64,0)` | YES |  |  |

#### `public.email_reminder_config`

- **Type:** BASE TABLE  **Rows:** 31

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('email_reminder_config_id_seq... | PK |
| `user_uuid` | `character varying(50)` | NO |  |  |
| `company_uuid` | `character varying(50)` | NO |  |  |
| `is_disabled` | `boolean` | NO | false |  |

#### `public.email_reminder_documents`

- **Type:** BASE TABLE  **Rows:** 79

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('email_reminder_documents_id_... | PK |
| `doc_type` | `character varying(11)` | NO |  |  |
| `doc_uuid` | `character varying(50)` | NO |  |  |
| `company_uuid` | `character varying(50)` | NO |  |  |
| `current_approval_group` | `character varying(50)` | NO |  |  |
| `last_sent_date` | `timestamp without time zone` | YES | now() |  |

**Indexes:**
- `email_reminder_documents_doc_type_doc_uuid`: `CREATE INDEX email_reminder_documents_doc_type_doc_uuid ON public.email_reminder_documents USING btree (doc_type, doc_uuid)`

#### `public.erp_api_configuration`

- **Type:** BASE TABLE  **Rows:** 4

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `company_uuid` | `character varying(100)` | NO |  |  |
| `api_type` | `character varying(250)` | NO |  |  |
| `api_url` | `character varying(250)` | NO |  |  |
| `user_name` | `character varying(100)` | YES |  |  |
| `password` | `character varying(100)` | YES |  |  |
| `id` | `integer(32,0)` | NO | nextval('erp_api_configuration_id_seq... |  |

**Indexes:**
- `erp_api_configuration_company_api_type_idx`: `CREATE UNIQUE INDEX erp_api_configuration_company_api_type_idx ON public.erp_api_configuration USING btree (company_uuid, api_type)`

#### `public.et_payment_settings`

- **Type:** BASE TABLE  **Rows:** 1359

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('et_payment_settings_id_seq':... | PK |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `payment_setting` | `integer(32,0)` | YES |  | FK → `public.payment_settings.id` |
| `created_at` | `timestamp with time zone` | YES |  |  |
| `updated_at` | `timestamp with time zone` | YES |  |  |

**Indexes:**
- `et_payment_settings_id_uindex`: `CREATE UNIQUE INDEX et_payment_settings_id_uindex ON public.et_payment_settings USING btree (id)`

#### `public.feature_column_state`

- **Type:** BASE TABLE  **Rows:** 1386

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('feature_column_state_id_seq'... | PK |
| `col_id` | `character varying(255)` | NO |  |  |
| `width` | `integer(32,0)` | YES |  |  |
| `hide` | `boolean` | YES | false |  |
| `pined` | `character varying(255)` | YES |  |  |
| `sort` | `character varying(255)` | YES |  |  |
| `sort_index` | `integer(32,0)` | YES |  |  |
| `agg_func` | `character varying(255)` | YES |  |  |
| `row_group` | `boolean` | YES | false |  |
| `row_group_index` | `integer(32,0)` | YES |  |  |
| `pivot` | `boolean` | YES | false |  |
| `pivot_index` | `integer(32,0)` | YES |  |  |
| `flex` | `integer(32,0)` | YES |  |  |
| `feature_state_id` | `bigint(64,0)` | YES |  | FK → `public.feature_state.id` |
| `col_index` | `integer(32,0)` | YES |  |  |

#### `public.feature_state`

- **Type:** BASE TABLE  **Rows:** 63

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('feature_state_id_seq'::regcl... | PK |
| `user_uuid` | `character varying(255)` | NO |  |  |
| `is_pivot_mode` | `boolean` | YES | false |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `state_label` | `character varying(50)` | YES |  |  |

#### `public.financial_institution`

- **Type:** BASE TABLE  **Rows:** 9

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('financial_institution_id_seq... | PK |
| `fi_code` | `character varying(50)` | NO |  |  |
| `fi_name` | `character varying(50)` | YES |  |  |
| `status` | `character varying(20)` | YES | 'ASSOCIATED'::character varying |  |
| `full_name` | `character varying(255)` | YES |  |  |
| `fi_uuid` | `character varying(255)` | YES |  |  |

**Indexes:**
- `financial_institution_fi_code_key`: `CREATE UNIQUE INDEX financial_institution_fi_code_key ON public.financial_institution USING btree (fi_code)`

#### `public.general_ledger`

- **Type:** BASE TABLE  **Rows:** 10769

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('general_ledger_id_seq'::regc... | PK |
| `account_number` | `character varying(20)` | YES |  |  |
| `description` | `character varying(200)` | YES |  |  |
| `is_active` | `boolean` | YES | true |  |
| `company_uuid` | `character varying(100)` | YES |  |  |
| `uuid` | `character varying(100)` | YES |  |  |
| `created_on` | `timestamp with time zone` | YES | now() |  |
| `updated_on` | `timestamp with time zone` | YES | now() |  |
| `is_deleted` | `boolean` | NO | false |  |
| `is_used` | `boolean` | NO | false |  |

**Indexes:**
- `general_ledger_index`: `CREATE INDEX general_ledger_index ON public.general_ledger USING btree (account_number, company_uuid)`
- `gl_index`: `CREATE INDEX gl_index ON public.general_ledger USING btree (company_uuid)`

#### `public.goods_receivers`

- **Type:** BASE TABLE  **Rows:** 0

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('goods_receivers_id_seq'::reg... | PK |
| `user_uuid` | `character varying(100)` | YES |  |  |
| `approval_matrix_id` | `bigint(64,0)` | YES |  | FK → `public.approval_matrix.id` |
| `name` | `character varying(100)` | YES |  |  |

#### `public.group_audit_trail`

- **Type:** BASE TABLE  **Rows:** 681

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('group_audit_trail_id_seq'::r... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `action` | `character varying(255)` | YES |  |  |
| `date_time` | `timestamp with time zone` | NO | now() |  |
| `previous_group_info` | `character varying(255)` | YES |  |  |
| `current_group_info` | `character varying(255)` | YES |  |  |
| `group_id` | `bigint(64,0)` | YES |  | FK → `public.groups.id` |

#### `public.group_users`

- **Type:** BASE TABLE  **Rows:** 5031

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('group_users_id_seq'::regclass) | PK |
| `group_id` | `bigint(64,0)` | YES |  | FK → `public.groups.id` |
| `user_uuid` | `character varying(100)` | YES |  |  |
| `name` | `character varying(100)` | YES |  |  |

**Indexes:**
- `group_users_user_uuid_group_id_idx`: `CREATE INDEX group_users_user_uuid_group_id_idx ON public.group_users USING btree (user_uuid, group_id)`

#### `public.groups`

- **Type:** BASE TABLE  **Rows:** 4634

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('groups_id_seq'::regclass) | PK |
| `group_name` | `character varying(200)` | NO |  |  |
| `group_description` | `character varying(500)` | NO |  |  |
| `is_active` | `boolean` | YES | true |  |
| `company_uuid` | `character varying(100)` | YES |  |  |
| `uuid` | `character varying(50)` | YES |  |  |
| `created_on` | `timestamp with time zone` | YES |  |  |
| `updated_on` | `timestamp with time zone` | YES |  |  |
| `created_by_uuid` | `character varying(255)` | YES |  |  |
| `created_by_name` | `character varying(255)` | YES |  |  |
| `is_single_user` | `boolean` | YES | false |  |
| `num_approver` | `bigint(64,0)` | YES |  |  |

#### `public.isocountry_currency`

- **Type:** BASE TABLE  **Rows:** 244

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO |  | PK |
| `country_name` | `character varying(255)` | YES |  |  |
| `currency_name` | `character varying(255)` | YES |  |  |
| `iso_country_code` | `character varying(50)` | YES |  |  |
| `iso_currency_code` | `character varying(50)` | YES |  |  |

**Indexes:**
- `isocountry_currency_iso_country_code_uindex`: `CREATE UNIQUE INDEX isocountry_currency_iso_country_code_uindex ON public.isocountry_currency USING btree (iso_country_code)`

#### `public.kyc_onboard_response`

- **Type:** BASE TABLE  **Rows:** 0

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `category` | `text` | YES |  |  |
| `onboard_user_id` | `text` | YES |  |  |
| `status` | `text` | YES |  |  |
| `description` | `text` | YES |  |  |

#### `public.kyc_payment_response`

- **Type:** BASE TABLE  **Rows:** 0

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `category` | `text` | YES |  |  |
| `transactionId` | `text` | YES |  |  |
| `buyerId` | `text` | YES |  |  |
| `suppplierId` | `text` | YES |  |  |
| `status` | `text` | YES |  |  |
| `description` | `text` | YES |  |  |

#### `public.liquibase-changelog`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `character varying(255)` | NO |  |  |
| `author` | `character varying(255)` | NO |  |  |
| `filename` | `character varying(255)` | NO |  |  |
| `dateexecuted` | `timestamp without time zone` | NO |  |  |
| `orderexecuted` | `integer(32,0)` | NO |  |  |
| `exectype` | `character varying(10)` | NO |  |  |
| `md5sum` | `character varying(35)` | YES |  |  |
| `description` | `character varying(255)` | YES |  |  |
| `comments` | `character varying(255)` | YES |  |  |
| `tag` | `character varying(255)` | YES |  |  |
| `liquibase` | `character varying(20)` | YES |  |  |
| `contexts` | `character varying(255)` | YES |  |  |
| `labels` | `character varying(255)` | YES |  |  |
| `deployment_id` | `character varying(10)` | YES |  |  |

#### `public.liquibase-lock`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO |  | PK |
| `locked` | `boolean` | NO |  |  |
| `lockgranted` | `timestamp without time zone` | YES |  |  |
| `lockedby` | `character varying(255)` | YES |  |  |

**Indexes:**
- `LIQUIBASE-LOCK_PKEY`: `CREATE UNIQUE INDEX "LIQUIBASE-LOCK_PKEY" ON public."liquibase-lock" USING btree (id)`

#### `public.modules`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('modules_id_seq'::regclass) | PK |
| `module_name` | `character varying(25)` | NO |  |  |
| `parent_id` | `bigint(64,0)` | YES |  | FK → `public.modules.id` |
| `created_at` | `timestamp with time zone` | NO | now() |  |
| `updated_at` | `timestamp with time zone` | NO | now() |  |

**Indexes:**
- `modules_parent_index`: `CREATE INDEX modules_parent_index ON public.modules USING btree (parent_id)`

#### `public.mt_bank`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `code` | `character varying(255)` | NO |  | PK |
| `created_on` | `timestamp without time zone` | YES |  |  |
| `updated_on` | `timestamp without time zone` | YES |  |  |
| `name` | `character varying(255)` | YES |  |  |
| `mt_country_iso_code` | `character varying(255)` | YES |  |  |

#### `public.onboard_error`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('onboard_error_id_seq'::regcl... | PK |
| `error_code` | `character varying(50)` | NO |  |  |
| `error_description` | `text` | NO |  |  |
| `onboard_response_id` | `integer(32,0)` | NO |  | FK → `public.onboard_response.id` |

#### `public.onboard_response`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('onboard_response_id_seq'::re... | PK |
| `request_id` | `text` | NO |  |  |
| `on_board_user_id` | `text` | YES |  |  |
| `status` | `text` | YES |  |  |
| `message` | `text` | YES |  |  |

#### `public.payment_cycle`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('payment_cycle_id_seq'::regcl... | PK |
| `uuid` | `character varying(50)` | YES |  |  |
| `company_uuid` | `character varying(50)` | YES |  |  |
| `payment_cycle_code` | `character varying(50)` | YES |  |  |
| `payment_cycle_date` | `integer(32,0)` | YES |  |  |
| `description` | `character varying(500)` | YES |  |  |
| `updated_on` | `timestamp with time zone` | YES | now() |  |
| `updated_by_uuid` | `character varying(50)` | YES |  |  |
| `updated_by_name` | `character varying(255)` | YES |  |  |
| `created_on` | `timestamp with time zone` | YES | now() |  |
| `created_by_uuid` | `character varying(50)` | YES |  |  |
| `created_by_name` | `character varying(255)` | YES |  |  |
| `active` | `boolean` | YES | false |  |

**Indexes:**
- `payment_cycle_companyuuid_index`: `CREATE INDEX payment_cycle_companyuuid_index ON public.payment_cycle USING btree (company_uuid)`
- `payment_cycle_companyuuid_paymentcyclecode_index`: `CREATE INDEX payment_cycle_companyuuid_paymentcyclecode_index ON public.payment_cycle USING btree (company_uuid, payment_cycle_code)`
- `payment_cycle_companyuuid_uuid_index`: `CREATE INDEX payment_cycle_companyuuid_uuid_index ON public.payment_cycle USING btree (company_uuid, uuid)`

#### `public.payment_cycle_audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('payment_cycle_audit_trail_id... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(50)` | YES |  |  |
| `action` | `character varying(100)` | YES |  |  |
| `date_time` | `timestamp with time zone` | NO | now() |  |
| `payment_cycle_id` | `bigint(64,0)` | YES |  | FK → `public.payment_cycle.id` |

#### `public.payment_cycle_supplier`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('payment_cycle_supplier_id_se... | PK |
| `payment_cycle_id` | `bigint(64,0)` | YES |  | FK → `public.payment_cycle.id` |
| `suppliers_id` | `bigint(64,0)` | YES |  | FK → `public.suppliers.id` |

#### `public.payment_error`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('payment_error_id_seq'::regcl... | PK |
| `error_code` | `character varying(50)` | NO |  |  |
| `error_description` | `text` | NO |  |  |
| `payment_response_id` | `bigint(64,0)` | NO |  | FK → `public.payment_response_from_bpsp.id` |

#### `public.payment_response_from_bpsp`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO |  | PK |
| `request_id` | `character varying(255)` | NO |  |  |
| `supplier_id` | `character varying(255)` | YES |  |  |
| `buyer_id` | `character varying(255)` | YES |  |  |
| `transaction_id` | `character varying(255)` | YES |  |  |
| `status` | `character varying(50)` | YES |  |  |
| `message` | `text` | YES |  |  |

#### `public.payment_settings`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('payment_settings_id_seq'::re... | PK |
| `code` | `character varying(50)` | YES |  |  |
| `description` | `character varying(500)` | YES |  |  |
| `is_default` | `boolean` | YES | false |  |

**Indexes:**
- `payment_settings_id_uindex`: `CREATE UNIQUE INDEX payment_settings_id_uindex ON public.payment_settings USING btree (id)`

#### `public.payment_term`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('payment_term_id_seq'::regclass) | PK |
| `pt_name` | `character varying(50)` | NO |  |  |
| `pt_days` | `integer(32,0)` | YES |  |  |
| `pt_remarks` | `character varying(500)` | YES |  |  |
| `updated_on` | `timestamp with time zone` | NO | now() |  |
| `created_on` | `timestamp with time zone` | NO | now() |  |
| `updated_by_name` | `character varying(255)` | NO |  |  |
| `updated_by_user_uuid` | `character varying(255)` | YES |  |  |
| `created_by_name` | `character varying(255)` | NO |  |  |
| `created_by_user_uuid` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `uuid` | `character varying(255)` | NO |  |  |

#### `public.po_terms_and_conditions`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('po_terms_and_conditions_id_s... | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `code` | `character varying(255)` | YES |  |  |
| `label` | `character varying(255)` | YES |  |  |
| `is_default` | `boolean` | YES |  |  |
| `is_active` | `boolean` | YES |  |  |
| `terms_conditions` | `text` | YES |  |  |
| `is_deleted` | `boolean` | YES |  |  |
| `is_used` | `boolean` | YES |  |  |
| `created_on` | `timestamp without time zone` | YES | now() |  |
| `updated_on` | `timestamp without time zone` | YES |  |  |

**Indexes:**
- `po_terms_and_conditions_uuid_key`: `CREATE UNIQUE INDEX po_terms_and_conditions_uuid_key ON public.po_terms_and_conditions USING btree (uuid)`

#### `public.prefix_configurable_functions`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('prefix_configurable_function... | PK |
| `function_name` | `character varying(50)` | NO |  |  |
| `function_code` | `character varying(50)` | NO |  |  |
| `default_prefix` | `character varying(3)` | NO |  |  |
| `default_number_of_digits` | `integer(32,0)` | YES |  |  |
| `is_buyer_portal` | `boolean` | YES |  |  |

#### `public.prefix_generated_number`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('prefix_generated_number_id_s... | PK |
| `prefix_setup_id` | `bigint(64,0)` | YES |  | FK → `public.prefix_setup.id` |
| `generated_number` | `character varying(255)` | YES |  |  |

#### `public.prefix_project_running_number`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('prefix_project_running_numbe... | PK |
| `prefix_setup_id` | `bigint(64,0)` | YES |  | FK → `public.prefix_setup.id` |
| `project_code` | `character varying(255)` | YES |  |  |
| `current_number` | `bigint(64,0)` | YES |  |  |

#### `public.prefix_running_number`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('prefix_running_number_id_seq... | PK |
| `prefix_type` | `character varying(20)` | NO |  |  |
| `prefix_key` | `character varying(255)` | NO |  |  |
| `current_number` | `bigint(64,0)` | YES | 1 |  |
| `prefix_setup_id` | `bigint(64,0)` | NO |  | FK → `public.prefix_setup.id` |

**Indexes:**
- `prefix_running_number_idx`: `CREATE UNIQUE INDEX prefix_running_number_idx ON public.prefix_running_number USING btree (prefix_setup_id, prefix_type, prefix_key)`

#### `public.prefix_setup`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('prefix_setup_id_seq'::regclass) | PK |
| `prefix_configurable_function_id` | `bigint(64,0)` | YES |  | FK → `public.prefix_configurable_functions.id` |
| `type` | `character varying(50)` | NO |  |  |
| `prefix_sample_output` | `character varying(255)` | NO |  |  |
| `created_by_uuid` | `character varying(100)` | YES |  |  |
| `created_on` | `timestamp with time zone` | NO | now() |  |
| `updated_on` | `timestamp with time zone` | NO | now() |  |
| `prefix` | `character varying(3)` | YES |  |  |
| `is_project_code` | `boolean` | YES |  |  |
| `is_date_dynamic` | `boolean` | YES |  |  |
| `has_configure_before` | `boolean` | YES |  |  |
| `date_dynamic_prefix` | `character varying(100)` | YES |  |  |
| `number_of_digits` | `integer(32,0)` | YES |  |  |
| `starting_number` | `bigint(64,0)` | YES |  |  |
| `company_uuid` | `character varying(100)` | YES |  |  |
| `default_current_number` | `bigint(64,0)` | YES |  |  |
| `uuid` | `character varying(255)` | NO |  |  |
| `created_by` | `character varying(255)` | YES |  |  |
| `creator_designation` | `character varying(255)` | YES |  |  |

#### `public.prefix_setup_history`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('prefix_setup_history_id_seq'... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `action` | `character varying(255)` | YES |  |  |
| `actor_uuid` | `character varying(100)` | YES |  |  |
| `actor_name` | `character varying(255)` | YES |  |  |
| `actor_designation` | `character varying(255)` | YES |  |  |
| `timestamp` | `date` | YES | now() |  |
| `prefix_setup_id` | `integer(32,0)` | YES |  | FK → `public.prefix_setup.id` |

**Indexes:**
- `prefix_setup_history_id_uindex`: `CREATE UNIQUE INDEX prefix_setup_history_id_uindex ON public.prefix_setup_history USING btree (id)`
- `prefix_setup_history_pk`: `CREATE UNIQUE INDEX prefix_setup_history_pk ON public.prefix_setup_history USING btree (id)`

#### `public.prefix_supplier_running_number`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('prefix_supplier_running_numb... | PK |
| `prefix_setup_id` | `bigint(64,0)` | YES |  | FK → `public.prefix_setup.id` |
| `supplier_code` | `character varying(255)` | YES |  |  |
| `current_number` | `bigint(64,0)` | YES |  |  |

#### `public.price_audit_trail_catalogue`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('price_audit_trail_catalogue_... | PK |
| `unit_price` | `double precision` | YES |  |  |
| `uom_code` | `character varying(20)` | YES |  |  |
| `tax_code` | `character varying(50)` | YES |  |  |
| `tax_rate` | `double precision` | YES |  |  |
| `pricing_rfq_number` | `character varying(20)` | YES |  |  |
| `valid_from` | `date` | YES |  |  |
| `valid_to` | `date` | YES |  |  |
| `updated_at` | `timestamp without time zone` | YES |  |  |
| `updated_by` | `character varying(50)` | YES |  |  |
| `catalogue_id` | `bigint(64,0)` | NO |  | FK → `public.catalogues.id` |
| `reference_no` | `character varying(255)` | YES |  |  |
| `contracted_price` | `double precision` | YES |  |  |
| `unit_price_str` | `character varying(255)` | YES |  |  |
| `contracted_price_str` | `character varying(255)` | YES |  |  |

#### `public.prices`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('prices_id_seq'::regclass) | PK |
| `item_code` | `character varying(20)` | NO |  |  |
| `item_name` | `character varying(50)` | NO |  |  |
| `price_section` | `character varying(50)` | NO |  |  |
| `uom_code` | `character varying(20)` | NO |  |  |
| `currency_code` | `character varying(50)` | NO |  |  |
| `price` | `double precision` | NO | 0 |  |
| `item_description` | `character varying(500)` | YES |  |  |
| `company_uuid` | `character varying(100)` | NO |  |  |
| `updated_on` | `timestamp with time zone` | YES | now() |  |
| `updated_by_name` | `character varying(255)` | YES |  |  |
| `created_on` | `timestamp with time zone` | YES | now() |  |
| `created_by_name` | `character varying(255)` | YES |  |  |
| `active` | `boolean` | NO | true |  |
| `deleted` | `boolean` | NO | false |  |
| `in_used` | `boolean` | YES | false |  |
| `uom_id` | `bigint(64,0)` | YES |  | FK → `public.uom.id` |

**Indexes:**
- `price_company_uuid_index`: `CREATE INDEX price_company_uuid_index ON public.prices USING btree (company_uuid)`

#### `public.project_facility`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('project_facility_id_seq'::re... | PK |
| `facility_name` | `character varying(255)` | NO |  |  |
| `offer_date` | `timestamp without time zone` | NO | now() |  |
| `status` | `character varying(20)` | YES | 'ACTIVE'::character varying |  |
| `loan_account_number` | `character varying(255)` | NO |  |  |
| `project_account_no` | `character varying(20)` | NO | 1 |  |
| `project_code` | `character varying(255)` | YES |  |  |
| `project_id` | `bigint(64,0)` | YES |  | FK → `public.projects.id` |
| `financial_institution_id` | `integer(32,0)` | YES |  | FK → `public.financial_institution.id` |
| `uuid` | `character varying(100)` | YES |  |  |
| `company_uuid` | `character varying(100)` | YES |  |  |
| `created_at` | `timestamp without time zone` | YES |  |  |
| `updated_at` | `timestamp without time zone` | YES | now() |  |
| `created_by_uuid` | `character varying(256)` | YES |  |  |

**Indexes:**
- `project_facility_pk`: `CREATE UNIQUE INDEX project_facility_pk ON public.project_facility USING btree (id)`

#### `public.project_forecast_audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('project_forecast_audit_trail... | PK |
| `action` | `character varying(255)` | NO |  |  |
| `date_time` | `timestamp with time zone` | NO | now() |  |
| `comment` | `character varying(255)` | YES |  |  |
| `project_id` | `bigint(64,0)` | NO |  | FK → `public.projects.id` |
| `user_uuid` | `character varying(255)` | NO |  |  |
| `name` | `character varying(255)` | YES |  |  |
| `designation` | `character varying(255)` | YES |  |  |

#### `public.project_forecast_invoice_items`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('project_forecast_invoice_ite... | PK |
| `project_forecast_items_id` | `bigint(64,0)` | NO |  | FK → `public.project_forecast_items.id` |
| `invoice_item_id` | `bigint(64,0)` | YES |  |  |
| `invoice_no` | `character varying(255)` | YES |  |  |
| `invoice_uuid` | `character varying(255)` | YES |  |  |

#### `public.project_forecast_items`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('project_forecast_items_id_se... | PK |
| `item_code` | `character varying(50)` | NO |  |  |
| `item_name` | `character varying(200)` | NO |  |  |
| `description` | `text` | YES |  |  |
| `item_size` | `character varying(200)` | YES |  |  |
| `item_model` | `character varying(200)` | YES |  |  |
| `item_brand` | `character varying(200)` | YES |  |  |
| `uom_code` | `character varying(20)` | YES |  |  |
| `item_unit_price` | `double precision` | YES |  |  |
| `item_quantity` | `double precision` | YES |  |  |
| `total_contracted` | `double precision` | YES |  |  |
| `total_contracted_spend` | `double precision` | YES |  |  |
| `contract_pending_approval_invoices` | `double precision` | YES |  |  |
| `contract_approval_invoices` | `double precision` | YES |  |  |
| `contract_pending_billing` | `double precision` | YES |  |  |
| `total_noncontracted_spend` | `double precision` | YES |  |  |
| `noncontract_pending_approval_invoices` | `double precision` | YES |  |  |
| `noncontract_approval_invoices` | `double precision` | YES |  |  |
| `noncontract_pending_billing` | `double precision` | YES |  |  |
| `project_forecast_trades_id` | `bigint(64,0)` | YES |  | FK → `public.project_forecast_trades.id` |
| `manual_item` | `boolean` | YES |  |  |
| `source_currency` | `character varying(50)` | YES |  |  |
| `exchange_rate` | `double precision` | YES |  |  |
| `category_uuid` | `character varying(255)` | YES |  |  |
| `category_name` | `character varying(50)` | YES |  |  |
| `noncontract_gr_received` | `double precision` | YES | 0 |  |
| `in_use` | `boolean` | YES | false |  |
| `contract_gr_received` | `double precision` | YES | 0 |  |
| `cat_item_id` | `bigint(64,0)` | YES |  | FK → `public.catalogues.id` |
| `actual_committed` | `numeric(26,2)` | NO | 0 |  |
| `actual_invoiced` | `numeric(26,2)` | NO | 0 |  |
| `actual_accrual` | `numeric(26,2)` | NO | 0 |  |
| `po_number` | `character varying` | YES |  |  |
| `po_uuid` | `character varying` | YES |  |  |
| `wo_number` | `character varying` | YES |  |  |
| `wo_uuid` | `character varying` | YES |  |  |
| `vo_number` | `text` | YES |  |  |
| `vo_uuid` | `text` | YES |  |  |
| `po_item_id` | `bigint(64,0)` | YES |  |  |
| `invoice_item_id` | `bigint(64,0)` | YES |  |  |
| `uuid` | `character varying` | YES | uuid_generate_v4() |  |
| `project_id` | `integer(32,0)` | YES |  |  |
| `actual_claim_batched` | `numeric(26,2)` | NO | 0 |  |
| `claim_item_id` | `bigint(64,0)` | YES |  |  |
| `claim_batch_uuid` | `character varying(64)` | YES |  |  |
| `claim_batch_no` | `character varying(64)` | YES |  |  |

#### `public.project_forecast_trade_revision`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('project_forecast_trade_revis... | PK |
| `uuid` | `character varying` | NO |  |  |
| `trade_id` | `bigint(64,0)` | YES |  |  |
| `trade_code` | `character varying(255)` | YES |  |  |
| `trade_title` | `character varying(255)` | YES |  |  |
| `category_id` | `bigint(64,0)` | YES |  | FK → `public.category.id` |
| `project_id` | `bigint(64,0)` | NO |  | FK → `public.projects.id` |
| `initial_budget` | `numeric(26,2)` | YES |  |  |
| `initial_budget_str` | `character varying(255)` | YES |  |  |
| `revised_budget` | `numeric(26,2)` | YES |  |  |
| `revised_budget_str` | `character varying(255)` | YES |  |  |
| `forecast_amount` | `numeric(26,2)` | YES |  |  |
| `forecast_amount_str` | `character varying(255)` | YES |  |  |
| `actual_committed` | `numeric(26,2)` | YES |  |  |
| `actual_invoiced` | `numeric(26,2)` | YES |  |  |
| `actual_accrual` | `numeric(26,2)` | YES |  |  |
| `trade_path` | `character varying` | YES |  |  |
| `version` | `integer(32,0)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `user_name` | `character varying(255)` | YES |  |  |
| `serial_number` | `character varying(255)` | YES |  |  |
| `action` | `character varying(10)` | YES |  |  |
| `action_date` | `timestamp without time zone` | YES | now() |  |
| `actual_claim_batched` | `numeric(26,2)` | NO | 0 |  |

#### `public.project_forecast_trades`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('project_forecast_trades_id_s... | PK |
| `trade_code` | `character varying(20)` | YES |  |  |
| `trade_title` | `character varying(200)` | YES |  |  |
| `description` | `character varying(500)` | YES |  |  |
| `project_id` | `bigint(64,0)` | NO |  | FK → `public.projects.id` |
| `total_forecasted_source` | `double precision` | YES |  |  |
| `exchange_rate` | `double precision` | YES |  |  |
| `total_forecasted_document` | `double precision` | YES |  |  |
| `total_contracted` | `double precision` | YES |  |  |
| `total_contracted_spend` | `double precision` | YES |  |  |
| `contract_pending_approval_invoices` | `double precision` | YES |  |  |
| `contract_approval_invoices` | `double precision` | YES |  |  |
| `contract_pending_billing` | `double precision` | YES |  |  |
| `total_noncontracted_spend` | `double precision` | YES |  |  |
| `noncontract_pending_approval_invoices` | `double precision` | YES |  |  |
| `noncontract_approval_invoices` | `double precision` | YES |  |  |
| `noncontract_pending_billing` | `double precision` | YES |  |  |
| `noncontract_gr_received` | `double precision` | YES | 0 |  |
| `source_currency` | `character varying(255)` | YES |  |  |
| `total_spend` | `double precision` | YES | 0 |  |
| `initial_budget` | `numeric(26,2)` | NO | 0 |  |
| `revised_budget` | `numeric(26,2)` | NO | 0 |  |
| `forecast_amount` | `numeric(26,2)` | NO | 0 |  |
| `actual_committed` | `numeric(26,2)` | NO | 0 |  |
| `actual_invoiced` | `numeric(26,2)` | NO | 0 |  |
| `actual_accrual` | `numeric(26,2)` | NO | 0 |  |
| `trade_path` | `character varying` | YES | ''::character varying |  |
| `category_id` | `bigint(64,0)` | YES |  |  |
| `trade_id` | `bigint(64,0)` | YES |  |  |
| `uuid` | `character varying` | YES | uuid_generate_v4() |  |
| `initial_budget_str` | `character varying(255)` | YES |  |  |
| `revised_budget_str` | `character varying(255)` | YES |  |  |
| `forecast_amount_str` | `character varying(255)` | YES |  |  |
| `serial_number` | `character varying(255)` | YES |  |  |
| `actual_claim_batched` | `numeric(26,2)` | NO | 0 |  |

#### `public.project_users`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('project_users_id_seq'::regcl... | PK |
| `user_uuid` | `character varying(100)` | YES |  |  |
| `project_user_role` | `character varying(25)` | NO |  |  |
| `remarks` | `character varying(500)` | NO |  |  |
| `project_id` | `bigint(64,0)` | YES |  | FK → `public.projects.id` |
| `user_name` | `character varying(100)` | YES |  |  |

#### `public.projects`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('projects_id_seq'::regclass) | PK |
| `project_code` | `character varying(20)` | NO |  |  |
| `project_title` | `character varying(200)` | NO |  |  |
| `project_status` | `character varying(25)` | NO |  |  |
| `start_date` | `date` | YES |  |  |
| `end_date` | `date` | YES |  |  |
| `currency` | `character varying(100)` | NO |  |  |
| `project_description` | `character varying(1000)` | NO |  |  |
| `overall_budget` | `double precision` | YES |  |  |
| `approved_pr_budget` | `double precision` | YES |  |  |
| `issued_po_budget` | `double precision` | YES |  |  |
| `budget_used` | `double precision` | YES |  |  |
| `created_on` | `timestamp with time zone` | NO | now() |  |
| `created_by` | `character varying(50)` | NO |  |  |
| `updated_on` | `timestamp with time zone` | NO | now() |  |
| `updated_by` | `character varying(50)` | NO |  |  |
| `company_uuid` | `character varying(100)` | NO |  |  |
| `address_id` | `bigint(64,0)` | NO |  | FK → `public.addresses.id` |
| `uuid` | `character varying(100)` | YES |  |  |
| `erp_project_code` | `character varying(20)` | YES |  |  |
| `project_code_description` | `character varying(255)` | YES |  |  |
| `extended_date` | `date` | YES |  |  |
| `dtf_project_code` | `character varying` | YES |  |  |
| `dtf_tier_level` | `character varying(50)` | YES | 'SUBCONTRACTOR'::character varying |  |
| `last_active_status` | `character varying(255)` | YES |  |  |
| `last_active_address_uuid` | `character varying(255)` | YES |  |  |
| `is_jtc_configured` | `boolean` | NO | false |  |

#### `public.rates`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('rates_id_seq'::regclass) | PK |
| `company_uuid` | `character varying(100)` | YES |  |  |
| `loading_country` | `character varying(255)` | NO |  |  |
| `loading_port` | `character varying(255)` | NO |  |  |
| `discharge_country` | `character varying(255)` | NO |  |  |
| `discharge_port` | `character varying(255)` | NO |  |  |
| `destination` | `character varying(255)` | NO |  |  |
| `currency_code` | `character varying(255)` | NO |  |  |
| `twenty_gp` | `double precision` | YES |  |  |
| `fourty_gp` | `double precision` | YES |  |  |
| `fourty_hq` | `double precision` | YES |  |  |
| `fourty_five_hq` | `double precision` | YES |  |  |
| `mode` | `character varying(255)` | NO |  |  |
| `carrier` | `character varying(50)` | NO |  |  |
| `sc_no` | `character varying(50)` | NO |  |  |
| `valid_from` | `timestamp with time zone` | NO | now() |  |
| `valid_to` | `timestamp with time zone` | NO | now() |  |
| `internal_remark` | `character varying(500)` | YES |  |  |
| `external_remark` | `character varying(500)` | YES |  |  |
| `is_active` | `boolean` | YES | false |  |
| `is_deleted` | `boolean` | YES | false |  |
| `updated_on` | `timestamp with time zone` | YES | now() |  |
| `updated_by` | `character varying(100)` | YES |  |  |
| `created_on` | `timestamp with time zone` | YES | now() |  |
| `created_by` | `character varying(100)` | YES |  |  |
| `commodity` | `character varying(500)` | YES |  |  |

**Indexes:**
- `rate_company_uuid_index`: `CREATE INDEX rate_company_uuid_index ON public.rates USING btree (company_uuid)`

#### `public.service_txn_settings`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('service_txn_settings_id_seq'... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `feature` | `character varying(255)` | YES |  |  |

**Indexes:**
- `service_txn_settings_uuid_key`: `CREATE UNIQUE INDEX service_txn_settings_uuid_key ON public.service_txn_settings USING btree (uuid)`

#### `public.stateful_column`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('stateful_column_id_seq'::reg... | PK |
| `column_name` | `character varying(255)` | YES |  |  |
| `state_label` | `character varying(50)` | YES |  |  |
| `default_index` | `integer(32,0)` | YES |  |  |
| `default_width` | `integer(32,0)` | YES | 200 |  |
| `default_agg_func` | `character varying(255)` | YES | NULL::character varying |  |

#### `public.supplier_bank_account`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('supplier_bank_account_id_seq... | PK |
| `uuid` | `character varying(50)` | YES |  |  |
| `company_uuid` | `character varying(50)` | YES |  |  |
| `bank_label` | `character varying(255)` | YES |  |  |
| `country` | `character varying(255)` | YES |  |  |
| `bank_name` | `character varying(255)` | YES |  |  |
| `bank_account_no` | `character varying(255)` | YES |  |  |
| `account_holder_name` | `character varying(255)` | YES |  |  |
| `currency` | `character varying(255)` | YES |  |  |
| `swift_code` | `character varying(50)` | YES |  |  |
| `branch` | `character varying(255)` | YES |  |  |
| `branch_code` | `character varying(50)` | YES |  |  |
| `branch_city` | `character varying(255)` | YES |  |  |
| `branch_address_line1` | `character varying(255)` | YES |  |  |
| `branch_address_line2` | `character varying(255)` | YES |  |  |
| `postal_code` | `character varying(50)` | YES |  |  |
| `state_province` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `requestor_uuid` | `character varying(50)` | YES |  |  |
| `requestor_name` | `character varying(255)` | YES |  |  |
| `approver_uuid` | `character varying(50)` | YES |  |  |
| `approver_name` | `character varying(255)` | YES |  |  |
| `updated_on` | `timestamp with time zone` | YES | now() |  |
| `approved_date` | `timestamp with time zone` | YES |  |  |
| `default_account` | `boolean` | YES |  |  |
| `default_account_before_approval` | `boolean` | YES |  |  |
| `supplier_id` | `bigint(64,0)` | YES |  | FK → `public.suppliers.id` |
| `original_account_uuid` | `character varying(255)` | YES |  |  |
| `is_active` | `boolean` | YES | true |  |
| `account_type` | `character varying(200)` | YES |  |  |
| `full_name` | `character varying(255)` | YES |  |  |
| `email` | `character varying(255)` | YES |  |  |
| `work_number` | `character varying(100)` | YES |  |  |
| `designation` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |

**Indexes:**
- `supplier_bank_account_companyuuid_index`: `CREATE INDEX supplier_bank_account_companyuuid_index ON public.supplier_bank_account USING btree (company_uuid)`
- `supplier_bank_account_companyuuid_labelaccnoaccountholdername_i`: `CREATE INDEX supplier_bank_account_companyuuid_labelaccnoaccountholdername_i ON public.supplier_bank_account USING btree (company_uuid, bank_label, bank_account_no, account_holder_name)`
- `supplier_bank_account_companyuuid_uuid_index`: `CREATE INDEX supplier_bank_account_companyuuid_uuid_index ON public.supplier_bank_account USING btree (company_uuid, uuid)`

#### `public.supplier_bank_account_audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('supplier_bank_account_audit_... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(50)` | YES |  |  |
| `action` | `character varying(100)` | YES |  |  |
| `date_time` | `timestamp with time zone` | NO | now() |  |
| `approval_group` | `character varying(100)` | YES |  |  |
| `supplier_bank_account_id` | `bigint(64,0)` | YES |  | FK → `public.supplier_bank_account.id` |

#### `public.supplier_bank_account_document_metadata`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('supplier_bank_account_docume... | PK |
| `guid` | `character varying(50)` | YES |  |  |
| `file_label` | `character varying(50)` | YES |  |  |
| `file_description` | `character varying(255)` | YES |  |  |
| `uploaded_on` | `timestamp with time zone` | NO | now() |  |
| `uploaded_by` | `character varying(100)` | YES |  |  |
| `uploader_uuid` | `character varying(50)` | YES |  |  |
| `external_document` | `boolean` | YES |  |  |
| `supplier_bank_account_id` | `bigint(64,0)` | YES |  | FK → `public.supplier_bank_account.id` |

#### `public.supplier_users`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('supplier_users_id_seq'::regc... | PK |
| `full_name` | `character varying(255)` | YES |  |  |
| `email_address` | `character varying(255)` | YES |  |  |
| `country_code` | `character varying(255)` | YES |  |  |
| `work_number` | `character varying(255)` | YES |  |  |
| `is_default` | `boolean` | YES | false |  |
| `is_deleted` | `boolean` | YES | false |  |
| `supplier_id` | `bigint(64,0)` | YES |  | FK → `public.suppliers.id` |
| `uuid` | `character varying(255)` | YES | uuid_generate_v4() |  |

#### `public.suppliers`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('suppliers_id_seq'::regclass) | PK |
| `created_on` | `timestamp with time zone` | NO | now() |  |
| `is_deleted` | `boolean` | YES | false |  |
| `updated_on` | `timestamp with time zone` | NO | now() |  |
| `code` | `character varying(255)` | NO |  |  |
| `company_name` | `character varying(255)` | NO |  |  |
| `is_buyer` | `boolean` | YES |  |  |
| `is_connected` | `boolean` | YES |  |  |
| `is_seller` | `boolean` | YES |  |  |
| `system_status` | `boolean` | YES |  |  |
| `tax_number` | `character varying(255)` | YES |  |  |
| `created_by_uuid` | `character varying(255)` | YES |  |  |
| `updated_by_uuid` | `character varying(100)` | YES |  |  |
| `app_user_id` | `bigint(64,0)` | YES |  |  |
| `country_of_origin_iso_code` | `character varying(20)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `supplier_company_uuid` | `character varying(255)` | YES |  |  |
| `vendor_id` | `character varying(255)` | YES |  |  |
| `payment_terms` | `character varying(255)` | YES |  |  |
| `payment_id` | `bigint(64,0)` | YES |  |  |
| `is_created_from_supplier` | `boolean` | YES |  |  |
| `supplier_id` | `bigint(64,0)` | YES |  |  |
| `last_disconnected_date` | `timestamp with time zone` | YES |  |  |
| `is_permanent_added` | `boolean` | YES |  |  |
| `is_in_use` | `boolean` | YES |  |  |
| `calling_code` | `character varying(255)` | YES |  |  |
| `tax_code_is_active` | `boolean` | YES |  |  |
| `unique_entity_number` | `character varying(30)` | YES |  |  |
| `uen` | `character varying(50)` | NO |  |  |
| `gst_reg_no` | `character varying(50)` | YES |  |  |
| `uuid` | `character varying(255)` | NO |  |  |
| `bank_acc_receive_payment_id` | `bigint(64,0)` | YES |  | FK → `public.bank_account.id` |
| `payment_term_id` | `bigint(64,0)` | YES |  | FK → `public.payment_term.id` |
| `ap_specialist_id` | `bigint(64,0)` | YES |  | FK → `public.ap_specialist.id` |
| `country_of_origin` | `character varying(255)` | YES |  |  |
| `gst_reg_business` | `character varying(50)` | YES |  |  |
| `has_connection` | `boolean` | YES |  |  |
| `tax_id` | `bigint(64,0)` | YES |  | FK → `public.taxes.id` |
| `connection_status` | `character varying(255)` | YES |  |  |
| `original_uen` | `character varying(50)` | YES | NULL::character varying |  |
| `original_country_of_origin` | `character varying(255)` | YES | NULL::character varying |  |
| `is_va_result_fail` | `boolean` | YES | false |  |
| `erp_company_code` | `character varying(255)` | YES |  |  |
| `company_category_code` | `character varying(255)` | YES |  |  |

**Indexes:**
- `supplier_uuid_index`: `CREATE INDEX supplier_uuid_index ON public.suppliers USING btree (uuid)`

#### `public.task_management`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('task_management_id_seq'::reg... | PK |
| `task_name` | `character varying(25)` | NO |  |  |
| `task_code` | `character varying(25)` | NO |  |  |
| `module_id` | `bigint(64,0)` | YES |  | FK → `public.modules.id` |

**Indexes:**
- `task_management_task_code_index`: `CREATE INDEX task_management_task_code_index ON public.task_management USING btree (task_code)`

#### `public.taxes`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('taxes_id_seq'::regclass) | PK |
| `tax_code` | `character varying(50)` | YES |  |  |
| `tax_rate` | `double precision` | YES |  |  |
| `description` | `character varying(200)` | YES |  |  |
| `is_active` | `boolean` | YES | true |  |
| `company_uuid` | `character varying(100)` | YES |  |  |
| `update_on` | `timestamp with time zone` | YES | now() |  |
| `created_on` | `timestamp with time zone` | YES | now() |  |
| `uuid` | `character varying(100)` | NO | uuid_generate_v4() |  |
| `is_default` | `boolean` | YES | false |  |
| `is_deleted` | `boolean` | NO | false |  |
| `is_used` | `boolean` | NO | false |  |

**Indexes:**
- `tax_code_index`: `CREATE INDEX tax_code_index ON public.taxes USING btree (tax_code, company_uuid)`

#### `public.terms_and_conditions`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('terms_and_conditions_id_seq'... | PK |
| `company_uuid` | `character varying(100)` | YES |  |  |
| `terms_conditions` | `text` | YES |  |  |
| `updated_on` | `timestamp with time zone` | YES | now() |  |
| `updated_by` | `character varying(100)` | YES |  |  |
| `created_on` | `timestamp with time zone` | YES | now() |  |
| `created_by` | `character varying(100)` | YES |  |  |

**Indexes:**
- `terms_and_conditions_company_uuid_idx`: `CREATE UNIQUE INDEX terms_and_conditions_company_uuid_idx ON public.terms_and_conditions USING btree (company_uuid)`

#### `public.tiers`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('tiers_id_seq'::regclass) | PK |
| `company_uuid` | `character varying(100)` | YES |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `code` | `character varying(25)` | NO |  |  |
| `markup_value` | `double precision` | NO |  |  |
| `remarks` | `character varying(255)` | YES |  |  |
| `is_active` | `boolean` | YES | false |  |
| `is_default` | `boolean` | YES | false |  |
| `is_deleted` | `boolean` | YES | false |  |
| `updated_on` | `timestamp with time zone` | YES | now() |  |
| `updated_by` | `character varying(100)` | YES |  |  |
| `created_on` | `timestamp with time zone` | YES | now() |  |
| `created_by` | `character varying(100)` | YES |  |  |
| `markup_type` | `character varying(50)` | YES | 'PERCENTAGE'::character varying |  |

**Indexes:**
- `tier_company_uuid_index`: `CREATE INDEX tier_company_uuid_index ON public.tiers USING btree (company_uuid)`

#### `public.trades`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('trades_id_seq'::regclass) | PK |
| `trade_code` | `character varying(20)` | YES |  |  |
| `trade_title` | `character varying(200)` | YES |  |  |
| `description` | `character varying(500)` | YES |  |  |
| `is_active` | `boolean` | YES | true |  |
| `company_uuid` | `character varying(100)` | YES |  |  |
| `trade_code_uuid` | `character varying(100)` | YES |  |  |
| `created_by` | `character varying(255)` | YES |  |  |
| `created_by_uuid` | `character varying(255)` | YES |  |  |
| `created_on` | `timestamp with time zone` | NO | now() |  |
| `updated_on` | `timestamp with time zone` | YES | now() |  |
| `category_id` | `bigint(64,0)` | YES |  | FK → `public.category.id` |

#### `public.transaction_type`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('transaction_type_id_seq'::re... | PK |
| `uuid` | `character varying(64)` | NO |  |  |
| `company_uuid` | `character varying(64)` | NO |  |  |
| `code` | `character varying(100)` | NO |  |  |
| `name` | `character varying(255)` | YES |  |  |
| `description` | `text` | YES |  |  |
| `created_on` | `timestamp without time zone` | YES | now() |  |
| `created_by` | `character varying(100)` | YES |  |  |
| `updated_on` | `timestamp without time zone` | YES |  |  |
| `updated_by` | `character varying(100)` | YES |  |  |
| `is_active` | `boolean` | YES |  |  |

**Indexes:**
- `transaction_type_uuid_key`: `CREATE UNIQUE INDEX transaction_type_uuid_key ON public.transaction_type USING btree (uuid)`

#### `public.uom`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('uom_id_seq'::regclass) | PK |
| `uom_code` | `character varying(20)` | YES |  |  |
| `uom_name` | `character varying(50)` | YES |  |  |
| `description` | `character varying(200)` | YES |  |  |
| `is_active` | `boolean` | YES | true |  |
| `company_uuid` | `character varying(100)` | YES |  |  |
| `uuid` | `character varying(100)` | YES |  |  |
| `created_on` | `timestamp with time zone` | YES | now() |  |
| `updated_on` | `timestamp with time zone` | YES | now() |  |
| `is_deleted` | `boolean` | NO | false |  |
| `is_used` | `boolean` | NO | false |  |

**Indexes:**
- `uom_code_index`: `CREATE INDEX uom_code_index ON public.uom USING btree (uom_code, company_uuid)`

#### `public.vendors`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('vendors_id_seq'::regclass) | PK |
| `created_on` | `timestamp with time zone` | NO | now() |  |
| `is_deleted` | `boolean` | YES | false |  |
| `updated_on` | `timestamp with time zone` | NO | now() |  |
| `code` | `character varying(255)` | NO |  |  |
| `company_name` | `character varying(255)` | NO |  |  |
| `contact_person_email` | `character varying(255)` | NO |  |  |
| `contact_person_name` | `character varying(255)` | NO |  |  |
| `contact_person_work_number` | `character varying(50)` | NO |  |  |
| `is_buyer` | `boolean` | YES |  |  |
| `is_connected` | `boolean` | YES |  |  |
| `is_seller` | `boolean` | YES |  |  |
| `payment_term` | `character varying(255)` | NO |  |  |
| `system_status` | `boolean` | YES |  |  |
| `tax_number` | `character varying(255)` | YES |  |  |
| `created_by_id` | `bigint(64,0)` | YES |  |  |
| `updated_by_id` | `bigint(64,0)` | YES |  |  |
| `app_user_id` | `bigint(64,0)` | YES |  |  |
| `country_of_origin_iso_code` | `character varying(20)` | YES |  |  |
| `company_id` | `bigint(64,0)` | YES |  |  |
| `vendor_company_id` | `bigint(64,0)` | YES |  |  |
| `vendor_id` | `character varying(255)` | YES |  |  |
| `payment_terms` | `character varying(255)` | YES |  |  |
| `payment_id` | `bigint(64,0)` | YES |  |  |
| `is_created_from_supplier` | `boolean` | YES |  |  |
| `supplier_id` | `bigint(64,0)` | YES |  |  |
| `last_disconnected_date` | `timestamp with time zone` | YES |  |  |
| `is_permanent_added` | `boolean` | YES |  |  |
| `is_in_use` | `boolean` | YES |  |  |
| `calling_code` | `character varying(255)` | YES |  |  |
| `tax_code_is_active` | `boolean` | YES |  |  |
| `unique_entity_number` | `character varying(30)` | YES |  |  |
| `uen` | `character varying(50)` | NO |  |  |
| `gst_reg_business` | `character varying(50)` | NO |  |  |
| `gst_reg_no` | `character varying(50)` | YES |  |  |
| `uuid` | `character varying(255)` | NO |  |  |
| `ap_specialist` | `character varying(100)` | YES |  |  |

**Indexes:**
- `app_user_id_index`: `CREATE INDEX app_user_id_index ON public.vendors USING btree (app_user_id)`
- `company_id_index`: `CREATE INDEX company_id_index ON public.vendors USING btree (company_id)`
- `company_name_index`: `CREATE INDEX company_name_index ON public.vendors USING btree (company_name)`
- `contact_person_email_index`: `CREATE INDEX contact_person_email_index ON public.vendors USING btree (contact_person_email)`
- `vendor_company_id_index`: `CREATE INDEX vendor_company_id_index ON public.vendors USING btree (vendor_company_id)`
- `vendor_uuid_index`: `CREATE INDEX vendor_uuid_index ON public.vendors USING btree (uuid)`

---

## finance

**Schemas:** public
**Total tables:** 68

### Schema: `public`

#### `public.address`

- **Type:** BASE TABLE  **Rows:** 181

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('address_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `address_label` | `character varying(500)` | YES |  |  |
| `address_first_line` | `character varying(500)` | YES |  |  |
| `address_second_line` | `character varying(500)` | YES |  |  |
| `city` | `character varying(100)` | YES |  |  |
| `state` | `character varying(100)` | YES |  |  |
| `country` | `character varying(100)` | YES |  |  |
| `postal_code` | `character varying(20)` | YES |  |  |
| `md5_checksum` | `character varying(255)` | NO |  |  |

#### `public.approval_route`

- **Type:** BASE TABLE  **Rows:** 492

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('approval_route_id_seq'::regc... | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `code` | `character varying(255)` | NO |  |  |
| `sequence` | `character varying(500)` | NO |  |  |
| `next_group_uuid` | `character varying(255)` | YES |  |  |
| `next_group_name` | `character varying(500)` | YES |  |  |

#### `public.buyer`

- **Type:** BASE TABLE  **Rows:** 153

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('buyer_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `code` | `character varying(50)` | NO |  |  |
| `country` | `character varying(50)` | NO |  |  |
| `gst_no` | `character varying(50)` | YES |  |  |
| `company_reg_no` | `character varying(50)` | YES |  |  |
| `uen` | `character varying(50)` | NO |  |  |
| `md5_checksum` | `character varying(255)` | NO |  |  |
| `person_id` | `bigint(64,0)` | YES |  | FK → `public.person.id` |
| `address_id` | `bigint(64,0)` | YES |  | FK → `public.address.id` |
| `company_uuid` | `character varying(255)` | YES |  |  |

#### `public.co_collection_method`

- **Type:** BASE TABLE  **Rows:** 5

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('co_collection_method_id_seq1... | PK |
| `code` | `character varying(255)` | YES |  |  |
| `description` | `character varying(255)` | YES |  |  |
| `is_active` | `boolean` | YES |  |  |

#### `public.country`

- **Type:** BASE TABLE  **Rows:** 257

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `country_code` | `character varying(2)` | NO |  |  |
| `country_name` | `character varying(250)` | NO |  |  |
| `is_active` | `boolean` | YES | true |  |
| `id` | `integer(32,0)` | NO | nextval('country_id_seq1'::regclass) | PK |

#### `public.currencies`

- **Type:** BASE TABLE  **Rows:** 2

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('currencies_id_seq1'::regclass) | PK |
| `currency_code` | `character varying(50)` | NO |  |  |
| `currency_name` | `character varying(50)` | NO |  |  |
| `is_active` | `boolean` | YES | false |  |
| `is_default` | `boolean` | YES |  |  |
| `fi_code` | `bigint(64,0)` | YES |  | FK → `public.financial_institution.id` |

#### `public.currency`

- **Type:** BASE TABLE  **Rows:** 49

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('currency_id_seq'::regclass) | PK |
| `name` | `character varying(255)` | NO |  |  |
| `code` | `character varying(50)` | NO |  |  |
| `exchange_rate` | `double precision` | NO | 1 |  |
| `uuid` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | NO |  |  |

#### `public.databasechangeloglock`

- **Type:** BASE TABLE  **Rows:** 0

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO |  | PK |
| `locked` | `boolean` | NO |  |  |
| `lockgranted` | `timestamp without time zone` | YES |  |  |
| `lockedby` | `character varying(255)` | YES |  |  |

#### `public.dbp_approver_sendback_details`

- **Type:** BASE TABLE  **Rows:** 0

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('dbp_approver_sendback_detail... | PK |
| `reason` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `dbprequest_id` | `bigint(64,0)` | YES |  | FK → `public.developer_bank_processing.id` |
| `dbp_request_id` | `bigint(64,0)` | YES |  | FK → `public.developer_bank_processing.id` |

#### `public.dbp_payment_request_submission`

- **Type:** BASE TABLE  **Rows:** 0

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('dbp_payment_request_submissi... |  |
| `dbp_request_id` | `bigint(64,0)` | NO |  | FK → `public.developer_bank_processing.id` |
| `is_payment_request_submitted` | `character(1)` | NO |  |  |
| `submitted_on` | `timestamp without time zone` | YES |  |  |

**Indexes:**
- `dbp_payment_request_submission_un`: `CREATE UNIQUE INDEX dbp_payment_request_submission_un ON public.dbp_payment_request_submission USING btree (dbp_request_id)`

#### `public.dbp_request_approval`

- **Type:** BASE TABLE  **Rows:** 335

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('dbp_request_approval_id_seq1... | PK |
| `approved_by` | `character varying(255)` | YES |  |  |
| `approved_on` | `timestamp without time zone` | YES |  |  |
| `approver_comment` | `character varying(255)` | YES |  |  |
| `approver_group_name` | `character varying(255)` | YES |  |  |
| `approver_group_uuid` | `character varying(255)` | YES |  |  |
| `approver_sequence` | `character varying(255)` | YES |  |  |
| `approver_status` | `character varying(255)` | YES |  |  |
| `approver_uuid` | `character varying(255)` | YES |  |  |
| `dbp_request_id` | `bigint(64,0)` | YES |  | FK → `public.developer_bank_processing.id` |

#### `public.dbp_request_attachment`

- **Type:** BASE TABLE  **Rows:** 12

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('dbp_request_attachment_id_se... | PK |
| `file_description` | `character varying(255)` | YES |  |  |
| `file_label` | `character varying(255)` | YES |  |  |
| `guid` | `character varying(255)` | YES |  |  |
| `size` | `character varying(255)` | YES |  |  |
| `uploaded_by` | `character varying(255)` | YES |  |  |
| `uploaded_on` | `timestamp without time zone` | YES |  |  |
| `uploader_uuid` | `character varying(255)` | YES |  |  |
| `dbp_request_id` | `bigint(64,0)` | YES |  | FK → `public.developer_bank_processing.id` |
| `dbprequest_id` | `bigint(64,0)` | YES |  | FK → `public.developer_bank_processing.id` |
| `attachment` | `character varying(255)` | YES |  |  |
| `uuid` | `character varying(255)` | YES |  |  |

#### `public.dbp_request_bank_status`

- **Type:** BASE TABLE  **Rows:** 156

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('dbp_request_bank_status_id_s... | PK |
| `dbp_request_id` | `bigint(64,0)` | NO |  | FK → `public.developer_bank_processing.id` |
| `batch_id` | `character varying(100)` | NO |  |  |
| `encryptedilmscaseid` | `character varying(100)` | NO |  |  |
| `drawdown_date` | `character varying(8)` | NO |  |  |
| `status` | `character varying(100)` | YES |  |  |
| `bank_remarks` | `character varying(200)` | YES |  |  |
| `is_dbp_status_updated` | `character(1)` | NO |  |  |

**Indexes:**
- `dbp_request_bank_return_status_pk`: `CREATE UNIQUE INDEX dbp_request_bank_return_status_pk ON public.dbp_request_bank_status USING btree (id)`

#### `public.dbp_request_beneficiary`

- **Type:** BASE TABLE  **Rows:** 1696

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('dbp_request_beneficiary_id_s... | PK |
| `beneficiary_name` | `character varying(255)` | YES |  |  |
| `beneficiary_uuid` | `character varying(255)` | YES |  |  |

#### `public.dbp_request_beneficiary_view`

- **Type:** VIEW  **Rows:** —

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `rquuid` | `bigint(64,0)` | YES |  |  |
| `batchno` | `character varying(255)` | YES |  |  |
| `actioncode` | `text` | YES |  |  |
| `beneficiaryid` | `integer(32,0)` | YES |  |  |
| `beneficiaryname` | `character varying(255)` | YES |  |  |
| `uennumber` | `text` | YES |  |  |
| `suppliertaxid` | `character varying(255)` | YES |  |  |
| `countrycode` | `character varying(2)` | YES |  |  |
| `paymentmode` | `character varying(255)` | YES |  |  |
| `paymentdescription` | `character varying` | YES |  |  |
| `invoicetype` | `text` | YES |  |  |
| `invoicenumber` | `text` | YES |  |  |
| `totalinvoiceamount` | `numeric(19,2)` | YES |  |  |
| `isinvoiceamountgstapplicable` | `text` | YES |  |  |
| `payableamount` | `numeric(19,2)` | YES |  |  |
| `beneficiarybankname` | `character varying(255)` | YES |  |  |
| `beneficiarybankaccountno` | `character varying(255)` | YES |  |  |
| `beneficiarypayablename` | `character varying(255)` | YES |  |  |
| `beneficiarybankswiftcode` | `character varying(255)` | YES |  |  |
| `intermediarybankswiftcode` | `character varying(255)` | YES |  |  |
| `intermediarybankname` | `character varying(255)` | YES |  |  |
| `sortcode` | `character varying(255)` | YES |  |  |
| `cocollectionmethod` | `integer(32,0)` | YES |  |  |
| `beneficiaryaddressline1` | `character varying(255)` | YES |  |  |
| `beneficiaryaddressline2` | `character varying(255)` | YES |  |  |
| `beneficiaryaddressline3` | `character varying(255)` | YES |  |  |

#### `public.dbp_request_conversation`

- **Type:** BASE TABLE  **Rows:** 10

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('dbp_request_conversation_id_... | PK |
| `comment` | `character varying(255)` | YES |  |  |
| `date_time` | `timestamp without time zone` | YES |  |  |
| `external_conversation` | `boolean` | YES |  |  |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `dbp_request_id` | `bigint(64,0)` | YES |  | FK → `public.developer_bank_processing.id` |
| `dbprequest_id` | `bigint(64,0)` | YES |  | FK → `public.developer_bank_processing.id` |
| `reason` | `character varying(255)` | YES |  |  |

#### `public.dbp_request_defect`

- **Type:** BASE TABLE  **Rows:** 320

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('dbp_request_defect_id_seq1':... | PK |
| `defect_type_code` | `character varying(100)` | NO |  | FK → `public.defect_type.code` |
| `defect_id` | `character varying(100)` | NO |  |  |
| `document_type_code` | `character varying(20)` | YES |  |  |
| `file_reference_no` | `character varying(20)` | YES |  |  |
| `defect_category` | `integer(32,0)` | YES |  |  |
| `defect_remark` | `character varying(200)` | YES |  |  |
| `last_updated` | `timestamp without time zone` | YES | now() |  |
| `dbp_request_id` | `bigint(64,0)` | NO |  | FK → `public.developer_bank_processing.id` |
| `is_defect_updated` | `character(1)` | YES |  |  |

#### `public.dbp_request_defect_new`

- **Type:** BASE TABLE  **Rows:** 0

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('dbp_request_defect_new_id_se... | PK |
| `defect_type_code` | `character varying(100)` | NO |  | FK → `public.defect_type.code` |
| `defect_id` | `character varying(100)` | NO |  |  |
| `document_type_code` | `character varying(20)` | NO |  |  |
| `file_reference_no` | `character varying(20)` | NO |  |  |
| `defect_category` | `integer(32,0)` | YES |  |  |
| `defect_remark` | `character varying(200)` | NO |  |  |
| `last_updated` | `timestamp without time zone` | YES | now() |  |
| `is_rectified` | `character(1)` | NO |  |  |
| `batch_no` | `character varying(20)` | NO |  |  |
| `dbp_request_id` | `bigint(64,0)` | NO |  | FK → `public.developer_bank_processing.id` |

#### `public.dbp_request_document`

- **Type:** BASE TABLE  **Rows:** 1624

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('dbp_request_document_id_seq1... | PK |
| `file_description` | `character varying(255)` | YES |  |  |
| `external_document` | `boolean` | YES |  |  |
| `file_label` | `character varying(255)` | YES |  |  |
| `guid` | `character varying(255)` | YES |  |  |
| `uploaded_by` | `character varying(255)` | YES |  |  |
| `uploaded_on` | `timestamp without time zone` | YES |  |  |
| `uploader_uuid` | `character varying(255)` | YES |  |  |
| `version` | `character varying(255)` | YES |  |  |
| `dbp_request_id` | `bigint(64,0)` | YES |  | FK → `public.developer_bank_processing.id` |
| `document_type_id` | `bigint(64,0)` | YES |  | FK → `public.document_type.id` |
| `dbprequest_id` | `bigint(64,0)` | YES |  | FK → `public.developer_bank_processing.id` |
| `remark` | `character varying(255)` | YES |  |  |
| `size` | `character varying(255)` | YES |  |  |
| `updated_on` | `timestamp without time zone` | YES |  |  |
| `is_document_sent_to_bank` | `character(1)` | YES |  |  |
| `dbp_beneficiary_id` | `bigint(64,0)` | YES |  | FK → `public.dbp_request_beneficiary.id` |
| `signed_doc_bytes` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |

#### `public.dbp_request_document_list_update_view`

- **Type:** VIEW  **Rows:** —

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `rquuid` | `bigint(64,0)` | YES |  |  |
| `batchno` | `character varying(255)` | YES |  |  |
| `seqno` | `text` | YES |  |  |
| `filecategory` | `text` | YES |  |  |
| `flag` | `text` | YES |  |  |
| `uploadedby` | `character varying(255)` | YES |  |  |
| `uploadversion` | `character varying(255)` | YES |  |  |
| `beneficiaryname` | `text` | YES |  |  |
| `filereferenceno` | `text` | YES |  |  |
| `guid` | `character varying(255)` | YES |  |  |
| `filename` | `text` | YES |  |  |
| `fileattachment` | `text` | YES |  |  |
| `filetype` | `character varying(10)` | YES |  |  |
| `documenttypecode` | `character varying(100)` | YES |  |  |
| `encryptedilmscaseid` | `text` | YES |  |  |
| `defectid` | `text` | YES |  |  |

#### `public.dbp_request_document_list_view`

- **Type:** VIEW  **Rows:** —

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `rquuid` | `bigint(64,0)` | YES |  |  |
| `batchno` | `character varying(255)` | YES |  |  |
| `seqno` | `text` | YES |  |  |
| `filecategory` | `text` | YES |  |  |
| `flag` | `text` | YES |  |  |
| `uploadedby` | `character varying(255)` | YES |  |  |
| `uploadversion` | `character varying(255)` | YES |  |  |
| `beneficiaryname` | `text` | YES |  |  |
| `filereferenceno` | `text` | YES |  |  |
| `guid` | `character varying(255)` | YES |  |  |
| `filename` | `text` | YES |  |  |
| `fileattachment` | `text` | YES |  |  |
| `filetype` | `character varying(10)` | YES |  |  |
| `documenttypecode` | `character varying(100)` | YES |  |  |
| `encryptedilmscaseid` | `text` | YES |  |  |
| `defectid` | `text` | YES |  |  |

#### `public.dbp_request_drawdown_amount`

- **Type:** BASE TABLE  **Rows:** 504

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('dbp_request_drawdown_amount_... | PK |
| `currency` | `character varying(255)` | YES |  |  |
| `current_account_amount` | `numeric(19,2)` | YES |  |  |
| `loan_account_amount` | `numeric(19,2)` | YES |  |  |
| `project_account_amount` | `numeric(19,2)` | YES |  |  |
| `total_batch_amount` | `numeric(19,2)` | YES |  |  |

#### `public.dbp_request_invoice`

- **Type:** BASE TABLE  **Rows:** 831

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('dbp_request_invoice_id_seq1'... | PK |
| `approval_sequence` | `character varying(255)` | YES |  |  |
| `approved_by_uuid` | `character varying(255)` | YES |  |  |
| `approved_date` | `character varying(255)` | YES |  |  |
| `architect_certificate_amount` | `numeric(19,2)` | YES |  |  |
| `currency` | `character varying(255)` | YES |  |  |
| `dbp_request_id` | `bigint(64,0)` | YES |  | FK → `public.developer_bank_processing.id` |
| `invoice_no` | `character varying(255)` | YES |  |  |
| `invoice_type` | `character varying(255)` | YES |  |  |
| `invoice_uuid` | `character varying(255)` | YES |  |  |
| `is_gst_applicable` | `boolean` | YES |  |  |
| `paid_amount` | `numeric(19,2)` | YES |  |  |
| `payment_mode` | `character varying(255)` | YES |  |  |
| `supplier_name` | `character varying(255)` | YES |  |  |
| `total_invoice_amount` | `numeric(19,2)` | YES |  |  |
| `dbp_request_supplier_id` | `bigint(64,0)` | YES |  |  |
| `supplier_uuid` | `character varying(255)` | YES |  |  |
| `invoice_src` | `character varying(50)` | YES | 'DVPC_INVOICE_PROJECT'::character var... |  |

#### `public.dbp_request_payment_api_response`

- **Type:** BASE TABLE  **Rows:** 335

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('dbp_request_payment_api_resp... | PK |
| `dbp_request_id` | `bigint(64,0)` | YES |  | FK → `public.developer_bank_processing.id` |
| `acknowledgement` | `character varying(100)` | NO |  |  |
| `externalref` | `character varying(255)` | YES |  |  |
| `errcode` | `character varying(60)` | YES |  |  |
| `errdescription` | `character varying(4000)` | YES |  |  |
| `created_on` | `timestamp without time zone` | NO | now() |  |
| `is_notified` | `character(1)` | YES |  |  |

**Indexes:**
- `dbp_request_payment_api_ir_resp_pk`: `CREATE UNIQUE INDEX dbp_request_payment_api_ir_resp_pk ON public.dbp_request_payment_api_response USING btree (id)`

#### `public.dbp_request_payment_email_job_table`

- **Type:** BASE TABLE  **Rows:** 263

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('dbp_request_payment_email_jo... |  |
| `dbp_request_id` | `bigint(64,0)` | NO |  | FK → `public.developer_bank_processing.id` |
| `request_status` | `character varying(50)` | NO |  |  |
| `email_date` | `timestamp without time zone` | YES |  |  |

**Indexes:**
- `dbp_request_payment_email_job_table_un`: `CREATE UNIQUE INDEX dbp_request_payment_email_job_table_un ON public.dbp_request_payment_email_job_table USING btree (dbp_request_id, request_status)`

#### `public.dbp_request_payment_info`

- **Type:** BASE TABLE  **Rows:** 409

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('dbp_request_payment_info_id_... | PK |
| `beneficiary_address_line_1` | `character varying(255)` | YES |  |  |
| `beneficiary_address_line_2` | `character varying(255)` | YES |  |  |
| `beneficiary_address_line_3` | `character varying(255)` | YES |  |  |
| `beneficiary_bank_account_no` | `character varying(255)` | YES |  |  |
| `beneficiary_bank_name` | `character varying(255)` | YES |  |  |
| `beneficiary_bank_swift_code` | `character varying(255)` | YES |  |  |
| `beneficiary_company_registration_no` | `character varying(255)` | YES |  |  |
| `beneficiary_name` | `character varying(255)` | YES |  |  |
| `beneficiary_payable_name` | `character varying(255)` | YES |  |  |
| `beneficiary_tax_no` | `character varying(255)` | YES |  |  |
| `beneficiary_type` | `character varying(255)` | YES |  |  |
| `co_collection_method` | `character varying(255)` | YES |  |  |
| `country` | `character varying(255)` | YES |  |  |
| `intermediary_bank_name` | `character varying(255)` | YES |  |  |
| `intermediary_bank_swift_code` | `character varying(255)` | YES |  |  |
| `payment_description` | `character varying(255)` | YES |  |  |
| `payment_mode` | `character varying(255)` | YES |  |  |
| `sort_code` | `character varying(255)` | YES |  |  |
| `dbp_request_id` | `bigint(64,0)` | YES |  | FK → `public.developer_bank_processing.id` |
| `dbprequest_id` | `bigint(64,0)` | YES |  | FK → `public.developer_bank_processing.id` |
| `supplier_uuid` | `character varying(255)` | YES |  |  |

#### `public.dbp_request_project_account_rule`

- **Type:** BASE TABLE  **Rows:** 120

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('dbp_request_project_account_... | PK |
| `dbp_request_id` | `bigint(64,0)` | YES |  | FK → `public.developer_bank_processing.id` |
| `project_account_rule` | `character varying(255)` | YES |  |  |

#### `public.dbp_request_project_facility`

- **Type:** BASE TABLE  **Rows:** 564

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('dbp_request_project_facility... | PK |
| `draw_down_date` | `timestamp without time zone` | YES |  |  |
| `facility_agreement_offer_date` | `timestamp without time zone` | YES |  |  |
| `facility_name` | `character varying(255)` | YES |  |  |
| `loan_account_number` | `character varying(255)` | YES |  |  |
| `loan_end_date` | `timestamp without time zone` | YES |  |  |
| `loan_type` | `character varying(255)` | YES |  |  |
| `project_account_no` | `character varying(255)` | YES |  |  |
| `loan_period_frequence` | `character varying(255)` | YES |  |  |
| `loan_period_number` | `integer(32,0)` | YES |  |  |

#### `public.dbp_request_supplier`

- **Type:** BASE TABLE  **Rows:** 0

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('dbp_request_supplier_id_seq1... | PK |
| `company_registration_no` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `contact_email` | `character varying(255)` | YES |  |  |
| `contact_name` | `character varying(255)` | YES |  |  |
| `contact_number` | `character varying(255)` | YES |  |  |
| `contact_uuid` | `character varying(255)` | YES |  |  |
| `country_code` | `character varying(255)` | YES |  |  |
| `country_name` | `character varying(255)` | YES |  |  |
| `vendor_code` | `character varying(255)` | YES |  |  |
| `vendor_name` | `character varying(255)` | YES |  |  |
| `vendor_uuid` | `character varying(255)` | YES |  |  |

#### `public.dbp_request_view`

- **Type:** VIEW  **Rows:** —

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `rquuid` | `bigint(64,0)` | YES |  |  |
| `batchno` | `character varying(255)` | YES |  |  |
| `datetimegroup` | `text` | YES |  |  |
| `devuennumber` | `text` | YES |  |  |
| `idtype` | `text` | YES |  |  |
| `idissuecountry` | `text` | YES |  |  |
| `developername` | `text` | YES |  |  |
| `developerbankid` | `text` | YES |  |  |
| `instructiontypeid` | `character varying(255)` | YES |  |  |
| `instructiontype` | `character varying` | YES |  |  |
| `instructiontype2id` | `integer(32,0)` | YES |  |  |
| `instructiontype2` | `character varying(255)` | YES |  |  |
| `projectname` | `character varying(255)` | YES |  |  |
| `projectacctno` | `character varying(255)` | YES |  |  |
| `projectaccountruleapplicable` | `text` | YES |  |  |
| `rules` | `character varying(255)` | YES |  |  |
| `nooftransactions` | `text` | YES |  |  |
| `facilityagreementdate` | `text` | YES |  |  |
| `facilityname` | `character varying(255)` | YES |  |  |
| `loanaccountno` | `character varying(255)` | YES |  |  |
| `currentaccountno` | `character varying(255)` | YES |  |  |
| `loantype` | `character varying(255)` | YES |  |  |
| `loanperiodno` | `integer(32,0)` | YES |  |  |
| `loanperiodfrequency` | `text` | YES |  |  |
| `loanenddate` | `text` | YES |  |  |
| `batchcurrency` | `character varying(255)` | YES |  |  |
| `totalbatchamount` | `numeric(19,2)` | YES |  |  |
| `totalamountdrawdownfromprojectaccount` | `numeric(19,2)` | YES |  |  |
| `totalamountdrawdownfromloanaccount` | `numeric(19,2)` | YES |  |  |
| `totalamountdrawdownfromcurrentaccount` | `numeric(19,2)` | YES |  |  |
| `architectcertclaimamount` | `numeric(19,2)` | YES |  |  |
| `costoverrunamount` | `numeric` | YES |  |  |
| `checklistdeclaration` | `text` | YES |  |  |
| `drawdowndate` | `text` | YES |  |  |
| `totaldoc` | `integer(32,0)` | YES |  |  |
| `transactionreference` | `text` | YES |  |  |

#### `public.defect_type`

- **Type:** BASE TABLE  **Rows:** 4

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO |  | PK |
| `code` | `character varying(255)` | YES |  |  |
| `description` | `character varying(255)` | YES |  |  |
| `is_active` | `boolean` | YES |  |  |

**Indexes:**
- `defect_category_un`: `CREATE UNIQUE INDEX defect_category_un ON public.defect_type USING btree (code)`

#### `public.developer_bank_processing`

- **Type:** BASE TABLE  **Rows:** 330

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('developer_bank_processing_id... | PK |
| `approval_route_name` | `character varying(255)` | YES |  |  |
| `approval_route_uuid` | `character varying(255)` | YES |  |  |
| `batch_id` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `currency` | `character varying(255)` | NO |  |  |
| `financial_institution_code` | `character varying(255)` | YES |  |  |
| `is_check_list_declared` | `boolean` | YES |  |  |
| `is_project_account_rule_applicable` | `boolean` | YES |  |  |
| `next_approver_group_name` | `character varying(255)` | YES |  |  |
| `next_approver_group_uuid` | `character varying(255)` | YES |  |  |
| `next_route_approver_name` | `character varying(255)` | YES |  |  |
| `next_route_approver_sequence` | `character varying(255)` | YES |  |  |
| `next_route_approver_uuid` | `character varying(255)` | YES |  |  |
| `project_code` | `character varying(255)` | YES |  |  |
| `project_title` | `character varying(255)` | YES |  |  |
| `request_id` | `character varying(255)` | NO |  |  |
| `requestor_id` | `character varying(255)` | YES |  |  |
| `requestor_name` | `character varying(255)` | YES |  |  |
| `requestor_uuid` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `submitted_date` | `timestamp without time zone` | YES |  |  |
| `dbp_draw_amount_amt_id` | `bigint(64,0)` | YES |  | FK → `public.dbp_request_drawdown_amount.id` |
| `financing_request_type_id` | `bigint(64,0)` | YES |  | FK → `public.financing_request_type.id` |
| `instruction_type_id` | `bigint(64,0)` | YES |  | FK → `public.instruction_type.id` |
| `dbp_request_project_rule_id` | `bigint(64,0)` | YES |  | FK → `public.project_account_rule.id` |
| `dbp_project_facility_id` | `bigint(64,0)` | YES |  | FK → `public.dbp_request_project_facility.id` |
| `approval_route_sequence` | `character varying(255)` | YES |  |  |
| `next_route_approval_sequence_no` | `character varying(255)` | YES |  |  |
| `docusign_account_id` | `character varying(255)` | YES |  |  |
| `docusign_envelepe_id` | `character varying(255)` | YES |  |  |
| `skip_esign` | `boolean` | YES | false |  |
| `dev_uen_number` | `character varying(255)` | YES |  |  |
| `approval_route_id` | `bigint(64,0)` | YES |  | FK → `public.approval_route.id` |
| `fi_remark` | `text` | YES |  |  |
| `invoices_no` | `character varying(500)` | YES |  |  |
| `uuid` | `character varying(50)` | YES | uuid_generate_v4() |  |
| `dbp_currency_id` | `bigint(64,0)` | YES |  | FK → `public.currency.id` |
| `financial_institution_id` | `bigint(64,0)` | YES |  | FK → `public.financial_institution.id` |
| `project_uuid` | `character varying(255)` | YES |  |  |
| `reason` | `text` | YES |  |  |

#### `public.developer_bank_processing_audit_trail`

- **Type:** BASE TABLE  **Rows:** 1980

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('developer_bank_processing_au... | PK |
| `action` | `character varying(255)` | YES |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `date_time` | `timestamp without time zone` | YES |  |  |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `dbp_request_id` | `bigint(64,0)` | YES |  | FK → `public.developer_bank_processing.id` |
| `dbprequest_id` | `bigint(64,0)` | YES |  | FK → `public.developer_bank_processing.id` |

#### `public.document_type`

- **Type:** BASE TABLE  **Rows:** 68

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('document_type_id_seq1'::regc... | PK |
| `document_type_code` | `character varying(100)` | NO |  |  |
| `version` | `character varying(10)` | YES |  |  |
| `esign_required` | `boolean` | YES |  |  |
| `size` | `character varying(10)` | NO |  |  |
| `type` | `character varying(10)` | NO |  |  |
| `instruction_type` | `integer(32,0)` | NO |  | FK → `public.instruction_type.id` |
| `document_type_description` | `character varying(200)` | YES |  |  |
| `is_mandatory` | `boolean` | YES |  |  |

**Indexes:**
- `document_type_pk`: `CREATE UNIQUE INDEX document_type_pk ON public.document_type USING btree (id)`
- `document_type_un`: `CREATE UNIQUE INDEX document_type_un ON public.document_type USING btree (document_type_code, instruction_type)`

#### `public.docusign_document`

- **Type:** BASE TABLE  **Rows:** 463

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('docusign_document_id_seq1'::... | PK |
| `category` | `character varying(255)` | YES |  |  |
| `document_type_code` | `character varying(255)` | YES |  |  |
| `document_uuid` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `document_id` | `character varying(255)` | YES |  |  |
| `envelope_id` | `bigint(64,0)` | YES |  | FK → `public.docusign_envelope.id` |
| `signed_document_url` | `character varying(2000)` | YES |  |  |

#### `public.docusign_envelope`

- **Type:** BASE TABLE  **Rows:** 251

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('docusign_envelope_id_seq1'::... | PK |
| `account_id` | `character varying(255)` | YES |  |  |
| `dbprequestid` | `bigint(64,0)` | YES |  |  |
| `envelope_id` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `certificate_guid` | `character varying(2000)` | YES |  |  |
| `certificate_url` | `character varying(1000)` | YES |  |  |
| `certificateurl` | `character varying(255)` | YES |  |  |

#### `public.docusign_signer`

- **Type:** BASE TABLE  **Rows:** 268

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('docusign_signer_id_seq1'::re... | PK |
| `signer_email` | `character varying(255)` | YES |  |  |
| `signer_name` | `character varying(255)` | YES |  |  |
| `envelope_id` | `bigint(64,0)` | YES |  | FK → `public.docusign_envelope.id` |

#### `public.email_template`

- **Type:** BASE TABLE  **Rows:** 35

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('email_template_id_seq'::regc... |  |
| `feature_code` | `character varying(50)` | YES |  |  |
| `action` | `character varying(50)` | YES |  |  |
| `subject` | `character varying(500)` | YES |  |  |
| `content` | `character varying` | YES |  |  |

#### `public.fi_cn_project`

- **Type:** BASE TABLE  **Rows:** 104

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('fi_cn_project_id_seq'::regcl... | PK |
| `financing_credit_note_id` | `bigint(64,0)` | NO |  | FK → `public.financing_credit_note.id` |
| `project_uuid` | `character varying(255)` | YES |  |  |
| `project_code` | `character varying(255)` | YES |  |  |
| `project_title` | `character varying(500)` | YES |  |  |

#### `public.fi_inv_project`

- **Type:** BASE TABLE  **Rows:** 782

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('fi_inv_project_id_seq'::regc... | PK |
| `financing_invoice_id` | `bigint(64,0)` | NO |  | FK → `public.financing_invoice.id` |
| `project_uuid` | `character varying(255)` | YES |  |  |
| `project_code` | `character varying(255)` | YES |  |  |
| `project_title` | `character varying(500)` | YES |  |  |

#### `public.fi_project`

- **Type:** BASE TABLE  **Rows:** 21

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `fi_id` | `integer(32,0)` | NO | nextval('fi_project_fi_id_seq1'::regc... | PK, FK → `public.financial_institution.id` |
| `project_id` | `integer(32,0)` | NO | nextval('fi_project_project_id_seq1':... | PK, FK → `public.project.id` |

#### `public.finance_sequence_no`

- **Type:** BASE TABLE  **Rows:** 762

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `sequence_no` | `character varying(255)` | NO |  | PK |
| `number_format` | `character varying(255)` | YES |  |  |

#### `public.financial_institution`

- **Type:** BASE TABLE  **Rows:** 32

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('financial_institution_id_seq... | PK |
| `fi_code` | `character varying(20)` | NO |  |  |
| `fi_name` | `character varying(100)` | YES |  |  |
| `status` | `character varying(20)` | YES | 'ASSOCIATED'::character varying |  |
| `email` | `character varying(100)` | YES |  |  |
| `work_phone` | `character varying(30)` | YES |  |  |
| `destination` | `character varying(100)` | YES |  |  |
| `remark` | `character varying(200)` | YES |  |  |
| `country_code` | `character varying(50)` | YES | 65 |  |
| `full_name` | `character varying(255)` | YES |  |  |
| `fullname` | `character varying(255)` | YES |  |  |
| `address_line1` | `character varying(250)` | YES |  |  |
| `address_line2` | `character varying(250)` | YES |  |  |
| `postal_code` | `character varying(50)` | YES |  |  |
| `country` | `character varying(250)` | YES |  |  |
| `fi_uuid` | `character varying(255)` | YES |  |  |

**Indexes:**
- `financial_institution_fi_code_key`: `CREATE UNIQUE INDEX financial_institution_fi_code_key ON public.financial_institution USING btree (fi_code)`

#### `public.financing_bank`

- **Type:** BASE TABLE  **Rows:** 185

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('financing_bank_id_seq'::regc... | PK |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `uuid` | `character varying(255)` | NO |  |  |
| `bank_label` | `character varying(255)` | NO |  |  |
| `bank_name` | `character varying(255)` | NO |  |  |
| `bank_account_no` | `character varying(255)` | NO |  |  |
| `account_holder_name` | `character varying(255)` | NO |  |  |
| `currency` | `character varying(50)` | NO |  |  |
| `payment_description` | `character varying(500)` | YES |  |  |
| `md5_checksum` | `character varying(255)` | NO |  |  |
| `address_id` | `bigint(64,0)` | YES |  | FK → `public.address.id` |
| `swift_code` | `character varying(255)` | YES |  |  |

#### `public.financing_credit_note`

- **Type:** BASE TABLE  **Rows:** 114

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('financing_credit_note_id_seq... | PK |
| `credit_note_no` | `character varying(255)` | NO |  |  |
| `credit_note_uuid` | `character varying(255)` | NO |  |  |
| `invoice_no` | `character varying(255)` | YES |  |  |
| `invoice_uuid` | `character varying(255)` | YES |  |  |
| `total_amount` | `numeric(26,2)` | NO | 0 |  |
| `sub_total` | `numeric(26,2)` | YES | 0 |  |
| `tax` | `numeric(26,2)` | YES | 0 |  |
| `applied_amount` | `numeric(26,2)` | YES | 0 |  |
| `credit_note_date` | `timestamp with time zone` | YES |  |  |
| `currency_code` | `character varying(255)` | YES |  |  |
| `project_code` | `character varying(255)` | YES |  |  |
| `invoice_financing_request_id` | `bigint(64,0)` | YES |  | FK → `public.invoice_financing_request.id` |
| `paid_amount` | `numeric(26,2)` | YES | 0 |  |
| `invoice_type` | `character varying(50)` | YES |  |  |

#### `public.financing_invoice`

- **Type:** BASE TABLE  **Rows:** 717

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('financing_invoice_id_seq'::r... | PK |
| `invoice_no` | `character varying(255)` | YES |  |  |
| `invoice_uuid` | `character varying(255)` | YES |  |  |
| `total_amount` | `numeric(26,2)` | NO | 0 |  |
| `paid_amount` | `numeric(26,2)` | YES | 0 |  |
| `sub_total` | `numeric(26,2)` | YES | 0 |  |
| `tax` | `numeric(26,2)` | YES | 0 |  |
| `amount_to_pay` | `numeric(26,12)` | YES | 0 |  |
| `pending_payment_amount` | `numeric(26,2)` | YES | 0 |  |
| `invoice_date` | `timestamp with time zone` | YES |  |  |
| `invoice_due_date` | `timestamp with time zone` | YES |  |  |
| `system_due_date` | `timestamp with time zone` | YES |  |  |
| `currency_code` | `character varying(255)` | YES |  |  |
| `project_code` | `character varying(255)` | YES |  |  |
| `invoice_financing_request_id` | `bigint(64,0)` | YES |  | FK → `public.invoice_financing_request.id` |
| `invoice_type` | `character varying(255)` | YES |  |  |
| `amount_to_pay_str` | `character varying(255)` | YES |  |  |

#### `public.financing_loan_settlement`

- **Type:** BASE TABLE  **Rows:** 85

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('financing_loan_settlement_id... | PK |
| `bank_uuid` | `character varying(255)` | NO |  |  |
| `bank_name` | `character varying(500)` | YES |  |  |
| `bank_account_no` | `character varying(255)` | YES |  |  |
| `bank_account_holder` | `character varying(500)` | YES |  |  |
| `payment_description` | `text` | YES |  |  |
| `md5_checksum` | `character varying(255)` | YES |  |  |
| `swift_code` | `character varying(255)` | YES |  |  |
| `bank_label` | `character varying(255)` | YES |  |  |

#### `public.financing_other_documents`

- **Type:** BASE TABLE  **Rows:** 23

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('financing_other_documents_id... | PK |
| `file_description` | `character varying(255)` | YES |  |  |
| `file_label` | `character varying(255)` | YES |  |  |
| `guid` | `character varying(255)` | YES |  |  |
| `remarks` | `character varying(255)` | YES |  |  |
| `size` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `uploaded_by` | `character varying(255)` | YES |  |  |
| `uploader_uuid` | `character varying(255)` | YES |  |  |
| `invoice_financing_request_id` | `bigint(64,0)` | YES |  | FK → `public.invoice_financing_request.id` |
| `uploaded_on` | `timestamp with time zone` | YES | now() |  |

#### `public.financing_pdf_documents`

- **Type:** BASE TABLE  **Rows:** 2185

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('financing_pdf_documents_id_s... | PK |
| `file_description` | `character varying(255)` | YES |  |  |
| `file_label` | `character varying(255)` | YES |  |  |
| `guid` | `character varying(255)` | YES |  |  |
| `url` | `character varying(500)` | YES |  |  |
| `remarks` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `invoice_financing_request_id` | `bigint(64,0)` | YES |  | FK → `public.invoice_financing_request.id` |
| `type` | `character varying(255)` | YES |  |  |

#### `public.financing_request_type`

- **Type:** BASE TABLE  **Rows:** 1

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO |  | PK |
| `code` | `character varying(255)` | NO |  |  |
| `is_active` | `boolean` | YES |  |  |
| `description` | `character varying` | YES |  |  |

**Indexes:**
- `request_type_pk`: `CREATE UNIQUE INDEX request_type_pk ON public.financing_request_type USING btree (id)`
- `request_type_un`: `CREATE UNIQUE INDEX request_type_un ON public.financing_request_type USING btree (code)`

#### `public.instruction_type`

- **Type:** BASE TABLE  **Rows:** 4

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('instruction_type_id_seq1'::r... | PK |
| `description` | `character varying(255)` | NO |  |  |
| `is_active` | `boolean` | YES |  |  |
| `code` | `character varying(255)` | YES |  |  |

**Indexes:**
- `instruction_code_un`: `CREATE UNIQUE INDEX instruction_code_un ON public.instruction_type USING btree (code)`
- `instruction_type_pk`: `CREATE UNIQUE INDEX instruction_type_pk ON public.instruction_type USING btree (id)`

#### `public.invoice_financing_payment_api_configuration`

- **Type:** BASE TABLE  **Rows:** 5

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `bank_code` | `character varying(100)` | NO |  |  |
| `api_url` | `character varying(250)` | NO |  |  |
| `user_name` | `character varying(100)` | YES |  |  |
| `password` | `character varying(100)` | YES |  |  |
| `id` | `integer(32,0)` | NO | nextval('sgtradex_payment_api_configu... | PK |
| `company_uuid` | `character varying(255)` | NO |  |  |

**Indexes:**
- `invoice_financing_payment_api_configuration_un`: `CREATE UNIQUE INDEX invoice_financing_payment_api_configuration_un ON public.invoice_financing_payment_api_configuration USING btree (bank_code, company_uuid)`

#### `public.invoice_financing_req_attachment`

- **Type:** BASE TABLE  **Rows:** 31

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('invoice_financing_req_attach... | PK |
| `guid` | `character varying(255)` | NO |  |  |
| `label` | `character varying(255)` | NO |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `description` | `character varying(255)` | NO |  |  |
| `uploaded_by` | `character varying(255)` | NO |  |  |
| `uploader_uuid` | `character varying(255)` | NO |  |  |
| `uploaded_on` | `character varying(255)` | NO |  |  |
| `external` | `boolean` | YES | false |  |
| `invoice_financing_request_id` | `bigint(64,0)` | NO |  | FK → `public.invoice_financing_request.id` |

#### `public.invoice_financing_req_audit_trail`

- **Type:** BASE TABLE  **Rows:** 1691

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('invoice_financing_req_audit_... | PK |
| `user_name` | `character varying(255)` | NO |  |  |
| `user_uuid` | `character varying(255)` | NO |  |  |
| `designation` | `character varying(255)` | YES |  |  |
| `action` | `character varying(50)` | NO |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `date_time` | `timestamp with time zone` | NO |  |  |
| `remark` | `text` | YES |  |  |
| `invoice_financing_request_id` | `integer(32,0)` | NO |  | FK → `public.invoice_financing_request.id` |

#### `public.invoice_financing_request`

- **Type:** BASE TABLE  **Rows:** 647

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('invoice_financing_request_id... | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `number` | `character varying(255)` | NO |  |  |
| `type` | `character varying(255)` | NO |  |  |
| `status` | `character varying(255)` | NO |  |  |
| `fi_id` | `bigint(64,0)` | YES |  | FK → `public.financial_institution.id` |
| `created_by_id` | `bigint(64,0)` | YES |  | FK → `public.person.id` |
| `vendor_id` | `bigint(64,0)` | YES |  | FK → `public.vendor.id` |
| `buyer_id` | `bigint(64,0)` | YES |  | FK → `public.buyer.id` |
| `approval_route_id` | `bigint(64,0)` | YES |  | FK → `public.approval_route.id` |
| `shipping_details_id` | `bigint(64,0)` | YES |  | FK → `public.shipping_details.id` |
| `currency_id` | `bigint(64,0)` | YES |  | FK → `public.currency.id` |
| `financing_bank_id` | `bigint(64,0)` | YES |  | FK → `public.financing_bank.id` |
| `created_at` | `timestamp with time zone` | NO |  |  |
| `updated_at` | `timestamp with time zone` | NO | CURRENT_TIMESTAMP |  |
| `approved_at` | `timestamp with time zone` | YES |  |  |
| `loan_period_frequency` | `character varying(50)` | NO |  |  |
| `loan_period_number` | `bigint(64,0)` | YES |  |  |
| `draw_down_date` | `timestamp with time zone` | YES |  |  |
| `loan_end_date` | `timestamp with time zone` | NO |  |  |
| `total_invoice_amt` | `numeric(26,2)` | NO | 0 |  |
| `total_applied_credit_note_amt` | `numeric(26,2)` | NO | 0 |  |
| `total_financing_amt` | `numeric(26,2)` | NO | 0 |  |
| `check_declaration` | `boolean` | YES | false |  |
| `skip_esign` | `boolean` | YES | false |  |
| `loan_disbursed_date` | `timestamp with time zone` | YES |  |  |
| `loan_interest` | `numeric(26,2)` | YES | 0 |  |
| `total_amt_disbursed` | `numeric(26,2)` | YES | 0 |  |
| `payment_mode` | `character varying(100)` | NO |  |  |
| `bank_viewed` | `boolean` | YES | false |  |
| `bank_approved_at` | `timestamp with time zone` | YES |  |  |
| `approved_loan_end_date` | `timestamp with time zone` | YES |  |  |
| `terms_and_condition` | `boolean` | YES | false |  |
| `term_and_condition_url` | `text` | YES |  |  |
| `invoices_no` | `text` | YES |  |  |
| `credit_notes_no` | `text` | YES |  |  |
| `fi_remark` | `text` | YES |  |  |
| `financing_loan_settlement_id` | `bigint(64,0)` | YES |  | FK → `public.financing_loan_settlement.id` |

**Indexes:**
- `invoice_financing_request_company_uuid_index`: `CREATE INDEX invoice_financing_request_company_uuid_index ON public.invoice_financing_request USING btree (company_uuid)`
- `invoice_financing_request_status_index`: `CREATE INDEX invoice_financing_request_status_index ON public.invoice_financing_request USING btree (status)`
- `invoice_financing_request_uuid_index`: `CREATE INDEX invoice_financing_request_uuid_index ON public.invoice_financing_request USING btree (uuid)`

#### `public.invoice_financing_request_status_from_bank`

- **Type:** BASE TABLE  **Rows:** 97

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('invoice_financing_request_st... | PK |
| `if_request_id` | `bigint(64,0)` | NO |  | FK → `public.invoice_financing_request.id` |
| `participant_request_id` | `character varying(100)` | YES |  |  |
| `participant_id` | `character varying(100)` | YES |  |  |
| `participant_name` | `character varying(100)` | YES |  |  |
| `participant_system_id` | `character varying(100)` | YES |  |  |
| `participant_system_name` | `character varying(100)` | YES |  |  |
| `participant_meta_data_ref_id` | `character varying(100)` | YES |  |  |
| `ifr_financing_approved_date` | `character varying(30)` | YES |  |  |
| `ifr_financing_start_date` | `character varying(30)` | YES |  |  |
| `ifr_financing_maturity_date` | `character varying(30)` | YES |  |  |
| `ifr_disbursement_date` | `character varying(30)` | YES |  |  |
| `ifr_application_status` | `character varying(100)` | NO |  |  |
| `verified` | `character varying(100)` | YES |  |  |
| `on_behalf_of` | `character varying(100)` | YES |  |  |
| `is_invoice_financing_status_updated` | `character(1)` | NO |  |  |
| `ifr_clientside_id` | `character varying(255)` | YES |  |  |
| `message` | `character varying(2000)` | YES |  |  |
| `ifr_submittimestamp` | `character varying(255)` | YES |  |  |

**Indexes:**
- `if_request_status_from_sgtradex_pk`: `CREATE UNIQUE INDEX if_request_status_from_sgtradex_pk ON public.invoice_financing_request_status_from_bank USING btree (id)`

#### `public.invoice_type`

- **Type:** BASE TABLE  **Rows:** 2

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('invoice_type_id_seq1'::regcl... | PK |
| `code` | `character varying(255)` | YES |  |  |
| `description` | `character varying(255)` | YES |  |  |
| `is_active` | `boolean` | YES |  |  |

#### `public.liquibase-changelog`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `character varying(255)` | NO |  |  |
| `author` | `character varying(255)` | NO |  |  |
| `filename` | `character varying(255)` | NO |  |  |
| `dateexecuted` | `timestamp without time zone` | NO |  |  |
| `orderexecuted` | `integer(32,0)` | NO |  |  |
| `exectype` | `character varying(10)` | NO |  |  |
| `md5sum` | `character varying(35)` | YES |  |  |
| `description` | `character varying(255)` | YES |  |  |
| `comments` | `character varying(255)` | YES |  |  |
| `tag` | `character varying(255)` | YES |  |  |
| `liquibase` | `character varying(20)` | YES |  |  |
| `contexts` | `character varying(255)` | YES |  |  |
| `labels` | `character varying(255)` | YES |  |  |
| `deployment_id` | `character varying(10)` | YES |  |  |

#### `public.liquibase-lock`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO |  | PK |
| `locked` | `boolean` | NO |  |  |
| `lockgranted` | `timestamp without time zone` | YES |  |  |
| `lockedby` | `character varying(255)` | YES |  |  |

**Indexes:**
- `LIQUIBASE-LOCK_PKEY`: `CREATE UNIQUE INDEX "LIQUIBASE-LOCK_PKEY" ON public."liquibase-lock" USING btree (id)`

#### `public.payment_api_configuration`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `bank_code` | `character varying(100)` | NO |  |  |
| `api_url` | `character varying(250)` | NO |  |  |
| `user_name` | `character varying(100)` | YES |  |  |
| `password` | `character varying(100)` | YES |  |  |
| `id` | `integer(32,0)` | NO | nextval('payment_api_configuration_id... |  |

#### `public.payment_mode`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('payment_mode_id_seq1'::regcl... | PK |
| `code` | `character varying(20)` | NO |  |  |
| `is_active` | `boolean` | YES |  |  |
| `description` | `character varying` | YES |  |  |

**Indexes:**
- `payment_code_un`: `CREATE UNIQUE INDEX payment_code_un ON public.payment_mode USING btree (code)`
- `payment_mode_pk`: `CREATE UNIQUE INDEX payment_mode_pk ON public.payment_mode USING btree (id)`

#### `public.person`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('person_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `designation` | `character varying(255)` | YES |  |  |
| `email` | `character varying(255)` | NO |  |  |
| `phone_number` | `character varying(12)` | NO |  |  |
| `country_code` | `character varying(5)` | NO |  |  |
| `md5_checksum` | `character varying(255)` | NO |  |  |

#### `public.project`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('project_id_seq1'::regclass) | PK |
| `project_code` | `character varying(100)` | NO |  |  |
| `project_title` | `character varying(100)` | NO |  |  |
| `company` | `character varying(100)` | YES |  |  |
| `project_status` | `character varying(20)` | NO | 'ACTIVE'::character varying |  |
| `status` | `character varying(20)` | NO |  |  |
| `company_name` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `uuid` | `character varying(255)` | YES |  |  |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |

#### `public.project_account_rule`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('project_account_rule_id_seq1... | PK |
| `project_account_rule` | `character varying(255)` | YES |  |  |
| `project_account_rule_applicable` | `boolean` | YES |  |  |

#### `public.project_facility`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('project_facility_id_seq1'::r... | PK |
| `facility_name` | `character varying(255)` | NO |  |  |
| `offer_date` | `timestamp without time zone` | NO | now() |  |
| `status` | `character varying(20)` | YES | 'ACTIVE'::character varying |  |
| `loan_account_number` | `character varying(255)` | NO |  |  |
| `project_account_no` | `character varying(20)` | NO | 1 |  |
| `project_code` | `character varying(255)` | YES |  |  |
| `project_id` | `bigint(64,0)` | YES |  | FK → `public.project.id` |

**Indexes:**
- `project_facility_pk`: `CREATE UNIQUE INDEX project_facility_pk ON public.project_facility USING btree (id)`

#### `public.project_facility__audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('project_facility__audit_trai... | PK |
| `action` | `character varying(255)` | YES |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `date_time` | `timestamp with time zone` | YES | now() |  |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `processing_req_id` | `bigint(64,0)` | YES |  |  |

#### `public.shipping_details`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('shipping_details_id_seq'::re... | PK |
| `carrier_name` | `character varying(255)` | YES |  |  |
| `consignee` | `character varying(255)` | YES |  |  |
| `goods_destination_location` | `character varying(255)` | YES |  |  |
| `goods_loading_location` | `character varying(255)` | YES |  |  |
| `incoterm` | `character varying(255)` | YES |  |  |
| `notify_party` | `character varying(255)` | YES |  |  |
| `remarks` | `character varying(500)` | YES |  |  |
| `shipper_name` | `character varying(255)` | YES |  |  |
| `transport_document_no` | `character varying(255)` | YES |  |  |
| `vessel_name` | `character varying(255)` | YES |  |  |
| `md5_checksum` | `character varying(255)` | YES |  |  |

#### `public.vendor`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('vendor_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `code` | `character varying(50)` | NO |  |  |
| `country` | `character varying(50)` | NO |  |  |
| `gst_no` | `character varying(50)` | YES |  |  |
| `company_reg_no` | `character varying(50)` | YES |  |  |
| `uen` | `character varying(50)` | NO |  |  |
| `md5_checksum` | `character varying(255)` | NO |  |  |
| `person_id` | `bigint(64,0)` | YES |  | FK → `public.person.id` |
| `address_id` | `bigint(64,0)` | YES |  | FK → `public.address.id` |
| `company_uuid` | `character varying(255)` | YES |  |  |

---

## invoices_uat

**Schemas:** public
**Total tables:** 64

### Schema: `public`

#### `public.addresses`

- **Type:** BASE TABLE  **Rows:** 1359

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('addresses_id_seq'::regclass) | PK |
| `address_label` | `character varying(500)` | NO |  |  |
| `address_first_line` | `character varying(500)` | NO |  |  |
| `address_second_line` | `character varying(200)` | YES |  |  |
| `city` | `character varying(100)` | YES |  |  |
| `state` | `character varying(100)` | NO |  |  |
| `country` | `character varying(100)` | NO |  |  |
| `postal_code` | `character varying(20)` | NO |  |  |
| `uuid` | `character varying(255)` | NO |  |  |
| `md5check_sum` | `character varying(500)` | YES |  |  |

**Indexes:**
- `address_uuid_index`: `CREATE INDEX address_uuid_index ON public.addresses USING btree (uuid)`

#### `public.bpr`

- **Type:** BASE TABLE  **Rows:** 325

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('bpr_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `fi_uuid` | `character varying(255)` | NO |  |  |
| `project_uuid` | `character varying(255)` | NO |  |  |
| `supplier_company_uuid` | `character varying(255)` | NO |  |  |
| `issue_vc` | `boolean` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `created_at` | `timestamp with time zone` | NO | now() |  |
| `wr_uuid` | `character varying(255)` | YES |  |  |

#### `public.bpsp`

- **Type:** BASE TABLE  **Rows:** 2200

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('bpsp_id_seq'::regclass) | PK |
| `request_id` | `text` | NO |  |  |
| `identifier` | `text` | YES |  |  |
| `payload` | `text` | NO |  |  |
| `type` | `text` | NO |  |  |
| `created_at` | `timestamp with time zone` | NO | now() |  |

#### `public.buyer_information`

- **Type:** BASE TABLE  **Rows:** 677

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('buyer_information_id_seq'::r... | PK |
| `buyer_code` | `character varying(255)` | YES |  |  |
| `buyer_uuid` | `character varying(255)` | YES |  |  |
| `company_name` | `character varying(255)` | YES |  |  |
| `buyer_company_uuid` | `character varying(100)` | YES |  |  |
| `gst_no` | `character varying(50)` | YES |  |  |
| `uen` | `character varying(50)` | YES |  |  |
| `md5check_sum` | `character varying(500)` | YES |  |  |
| `address_id` | `bigint(64,0)` | YES |  | FK → `public.addresses.id` |

#### `public.claim`

- **Type:** BASE TABLE  **Rows:** 1011

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('claim_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `claim_request_for` | `character varying(100)` | YES |  |  |
| `claim_category_uuid` | `character varying(100)` | YES |  |  |
| `claim_category_name` | `character varying(100)` | YES |  |  |
| `requester_uuid` | `character varying(100)` | YES |  |  |
| `invoice_no` | `character varying(255)` | YES |  |  |
| `status` | `character varying(100)` | YES |  |  |
| `remarks` | `text` | YES |  |  |
| `claim_no` | `character varying(255)` | YES |  |  |
| `currency` | `character varying(50)` | YES |  |  |
| `nature_of_request` | `character varying(100)` | YES |  |  |
| `creator_uuid` | `character varying(100)` | YES |  |  |
| `company_uuid` | `character varying(100)` | YES |  |  |
| `claim_date` | `timestamp with time zone` | YES |  |  |
| `created_on` | `timestamp with time zone` | NO | now() |  |
| `updated_on` | `timestamp with time zone` | NO | now() |  |
| `claim_amount` | `numeric(25,2)` | YES | 0 |  |
| `supplier_id` | `bigint(64,0)` | YES |  | FK → `public.supplier_information.id` |
| `creator_name` | `character varying(255)` | YES |  |  |
| `currency_name` | `character varying(100)` | YES |  |  |
| `aggregate_tax_amount` | `numeric(25,2)` | YES | 0 |  |
| `existed_vendor` | `boolean` | YES |  |  |
| `non_supplier_id` | `bigint(64,0)` | YES |  | FK → `public.non_supplier.id` |
| `user_claim_code` | `character varying(255)` | YES |  |  |

#### `public.claim_audit_trail`

- **Type:** BASE TABLE  **Rows:** 1770

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('claim_audit_trail_id_seq'::r... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `action` | `character varying(50)` | YES |  |  |
| `role` | `character varying(255)` | YES |  |  |
| `date` | `timestamp without time zone` | YES |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `claim_status` | `character varying(50)` | YES |  |  |
| `claim_id` | `bigint(64,0)` | NO |  | FK → `public.claim.id` |
| `claim_batch_no` | `character varying(255)` | YES |  |  |

#### `public.claim_batch`

- **Type:** BASE TABLE  **Rows:** 723

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('claim_batch_id_seq'::regclass) | PK |
| `uuid` | `character varying(100)` | YES |  |  |
| `claim_batch_no` | `character varying(255)` | YES |  |  |
| `claim_request_for` | `character varying(255)` | YES |  |  |
| `requester_uuid` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(100)` | YES |  |  |
| `creator_uuid` | `character varying(100)` | YES |  |  |
| `status` | `character varying(50)` | YES |  |  |
| `currency` | `character varying(50)` | YES |  |  |
| `approval_route_name` | `character varying(255)` | YES |  |  |
| `approval_route_sequence` | `character varying(255)` | YES |  |  |
| `approval_route_uuid` | `character varying(255)` | YES |  |  |
| `next_approver` | `character varying(255)` | YES |  |  |
| `next_approval_group_uuid` | `character varying(255)` | YES |  |  |
| `batch_amount` | `numeric(25,2)` | YES | 0 |  |
| `remarks` | `text` | YES |  |  |
| `claim_batch_date` | `timestamp with time zone` | YES |  |  |
| `created_on` | `timestamp with time zone` | NO | now() |  |
| `updated_on` | `timestamp with time zone` | NO | now() |  |
| `paid_amount` | `numeric(25,2)` | YES | 0 |  |
| `paid_payment_amount` | `numeric(25,2)` | YES | 0 |  |
| `paid_financing_amount` | `numeric(25,2)` | YES | 0 |  |
| `processing_amt` | `numeric(25,2)` | YES | 0 |  |
| `processing_payment_amt` | `numeric(25,2)` | YES | 0 |  |
| `processing_financing_amt` | `numeric(25,2)` | YES | 0 |  |
| `pending_payment_approval_amt` | `numeric(25,2)` | YES | 0 |  |
| `payment_number` | `character varying(255)` | YES |  |  |
| `payment_terms` | `character varying(255)` | YES |  |  |
| `payment_terms_uuid` | `character varying(255)` | YES |  |  |
| `payment_terms_days` | `integer(32,0)` | YES |  |  |
| `payment_notes` | `character varying(255)` | YES |  |  |
| `reissued_claim_batch_uuid` | `character varying(255)` | YES |  |  |
| `payment_status` | `character varying(255)` | YES |  |  |
| `currency_name` | `character varying(100)` | YES |  |  |
| `nature_of_request` | `character varying(100)` | YES |  |  |
| `claim_batch_approval_date` | `timestamp with time zone` | YES |  |  |
| `user_claim_code` | `character varying(255)` | YES |  |  |

#### `public.claim_batch_audit_trail`

- **Type:** BASE TABLE  **Rows:** 1225

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('claim_batch_audit_trail_id_s... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `action` | `character varying(255)` | YES |  |  |
| `role` | `character varying(255)` | YES |  |  |
| `date` | `timestamp without time zone` | YES |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `claim_batch_status` | `character varying(50)` | YES |  |  |
| `claim_batch_id` | `bigint(64,0)` | YES |  | FK → `public.claim_batch.id` |
| `payment_batch_uuid` | `character varying(255)` | YES |  |  |
| `payment_batch_no` | `character varying(255)` | YES |  |  |
| `payment_batch_amount` | `numeric(19,2)` | YES |  |  |

#### `public.claim_batch_item`

- **Type:** BASE TABLE  **Rows:** 790

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('claim_batch_item_id_seq'::re... | PK |
| `uuid` | `character varying(100)` | YES |  |  |
| `claim_no` | `character varying(255)` | YES |  |  |
| `sub_total` | `numeric(25,2)` | YES | 0 |  |
| `tax_amount` | `numeric(25,2)` | YES | 0 |  |
| `claim_amount` | `numeric(25,2)` | YES | 0 |  |
| `claim_category_uuid` | `character varying(100)` | YES |  |  |
| `claim_category_name` | `character varying(255)` | YES |  |  |
| `claim_batch_id` | `bigint(64,0)` | YES |  | FK → `public.claim_batch.id` |
| `claim_id` | `bigint(64,0)` | YES |  | FK → `public.claim.id` |

#### `public.claim_batch_processing_amt`

- **Type:** BASE TABLE  **Rows:** 187

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('claim_batch_processing_amt_i... | PK |
| `claim_batch_uuid` | `character varying(255)` | YES |  |  |
| `payment_no` | `character varying(255)` | YES |  |  |
| `payment_ref` | `character varying(255)` | YES |  |  |
| `payment_uuid` | `character varying(255)` | YES |  |  |
| `payment_status` | `character varying(255)` | YES |  |  |
| `amount_to_pay` | `numeric(25,2)` | YES | 0 |  |
| `claim_batch_id` | `bigint(64,0)` | YES |  | FK → `public.claim_batch.id` |
| `payment_batch_no` | `character varying(255)` | YES |  |  |
| `payment_batch_uuid` | `character varying(255)` | YES |  |  |
| `payment_release_date` | `timestamp with time zone` | YES |  |  |
| `total_batch_amount` | `numeric(25,2)` | YES | 0 |  |

#### `public.claim_batch_project_mapping`

- **Type:** BASE TABLE  **Rows:** 955

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('claim_batch_project_mapping_... | PK |
| `claim_batch_id` | `bigint(64,0)` | NO |  | FK → `public.claim_batch.id` |
| `project_id` | `bigint(64,0)` | NO |  | FK → `public.project.id` |

#### `public.claim_item`

- **Type:** BASE TABLE  **Rows:** 1966

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('claim_item_id_seq'::regclass) | PK |
| `uuid` | `character varying(100)` | YES |  |  |
| `cat_item_id` | `bigint(64,0)` | YES |  |  |
| `item_group` | `character varying(255)` | YES |  |  |
| `item_code` | `character varying(100)` | YES |  |  |
| `item_name` | `character varying(100)` | YES |  |  |
| `item_description` | `text` | YES |  |  |
| `model` | `character varying(255)` | YES |  |  |
| `size` | `character varying(255)` | YES |  |  |
| `brand` | `character varying(255)` | YES |  |  |
| `quantity` | `numeric(25,2)` | YES | 0 |  |
| `unit_price` | `numeric(25,2)` | YES | 0 |  |
| `sub_total_with_tax` | `numeric(25,2)` | YES | 0 |  |
| `sub_total` | `numeric(25,2)` | YES | 0 |  |
| `tax_code` | `character varying(100)` | YES |  |  |
| `tax_code_uuid` | `character varying(100)` | YES |  |  |
| `tax_rate` | `numeric(25,2)` | YES | 0 |  |
| `uom` | `character varying(100)` | YES |  |  |
| `uom_uuid` | `character varying(100)` | YES |  |  |
| `gl_account` | `character varying(100)` | YES |  |  |
| `gl_account_uuid` | `character varying(100)` | YES |  |  |
| `project_code` | `character varying(100)` | YES |  |  |
| `project_uuid` | `character varying(100)` | YES |  |  |
| `trade_code` | `character varying(255)` | YES |  |  |
| `trade_code_uuid` | `character varying(255)` | YES |  |  |
| `parent_uuid` | `character varying(100)` | YES |  |  |
| `have_children` | `boolean` | YES | false |  |
| `claim_id` | `bigint(64,0)` | YES |  | FK → `public.claim.id` |
| `parent_id` | `bigint(64,0)` | YES |  | FK → `public.claim_item.id` |
| `tax_amount` | `numeric(25,2)` | YES | 0 |  |
| `notes` | `text` | YES |  |  |
| `gl_description` | `character varying(255)` | YES |  |  |
| `cost_code` | `character varying(255)` | YES |  |  |
| `cost_code_remark` | `character varying(255)` | YES |  |  |
| `department_code` | `character varying(255)` | YES |  |  |
| `department_code_remark` | `character varying(255)` | YES |  |  |

#### `public.claim_project_mapping`

- **Type:** BASE TABLE  **Rows:** 1299

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('claim_project_mapping_id_seq... | PK |
| `claim_id` | `bigint(64,0)` | NO |  | FK → `public.claim.id` |
| `project_id` | `bigint(64,0)` | NO |  | FK → `public.project.id` |

#### `public.cn_project_mapping`

- **Type:** BASE TABLE  **Rows:** 688

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('cn_project_mapping_id_seq'::... | PK |
| `credit_note_id` | `bigint(64,0)` | NO |  | FK → `public.credit_note.id` |
| `project_id` | `bigint(64,0)` | NO |  | FK → `public.project.id` |

#### `public.consolidation_audit_trail`

- **Type:** BASE TABLE  **Rows:** 4

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('consolidation_audit_trail_id... | PK |
| `consolidation_id` | `bigint(64,0)` | NO |  | FK → `public.consolidation_summary.id` |
| `user_name` | `character varying(100)` | YES |  |  |
| `user_uuid` | `character varying(100)` | YES |  |  |
| `action` | `character varying(50)` | YES |  |  |
| `role` | `character varying(50)` | YES |  |  |
| `date` | `timestamp without time zone` | NO | CURRENT_TIMESTAMP |  |
| `approval_group` | `character varying(100)` | YES |  |  |
| `approval_group_uuid` | `character varying(100)` | YES |  |  |

#### `public.consolidation_summary`

- **Type:** BASE TABLE  **Rows:** 4

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('consolidation_summary_id_seq... | PK |
| `uuid` | `character varying(100)` | NO |  |  |
| `project_uuid` | `character varying(100)` | NO |  |  |
| `claim_month` | `timestamp without time zone` | NO |  |  |
| `created_at` | `timestamp without time zone` | NO | CURRENT_TIMESTAMP |  |
| `submitted_by` | `character varying(100)` | YES |  |  |
| `payment_reference_id` | `character varying(100)` | YES |  |  |
| `remark` | `text` | YES |  |  |
| `status` | `character varying(50)` | NO |  |  |

**Indexes:**
- `consolidation_summary_uuid_key`: `CREATE UNIQUE INDEX consolidation_summary_uuid_key ON public.consolidation_summary USING btree (uuid)`
- `uq_project_claim_month`: `CREATE UNIQUE INDEX uq_project_claim_month ON public.consolidation_summary USING btree (project_uuid, claim_month)`

#### `public.contact_person`

- **Type:** BASE TABLE  **Rows:** 752

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('contact_person_id_seq'::regc... | PK |
| `name` | `character varying(255)` | YES |  |  |
| `phone_number` | `character varying(255)` | YES |  |  |
| `country_code` | `character varying(50)` | YES |  |  |
| `email` | `character varying(500)` | YES |  |  |
| `md5check_sum` | `character varying(255)` | YES |  |  |
| `contact_person_uuid` | `character varying(255)` | YES |  |  |
| `supplier_uuid` | `character varying(255)` | YES |  |  |

**Indexes:**
- `contact_person_pk`: `CREATE UNIQUE INDEX contact_person_pk ON public.contact_person USING btree (id)`

#### `public.credit_note`

- **Type:** BASE TABLE  **Rows:** 971

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('credit_note_id_seq'::regclass) | PK |
| `credit_note_number` | `character varying(50)` | NO |  |  |
| `global_cn_number` | `character varying(50)` | NO |  |  |
| `status` | `character varying(255)` | NO |  |  |
| `credit_note_date` | `timestamp with time zone` | NO |  |  |
| `submission_date` | `timestamp with time zone` | NO | now() |  |
| `invoice_number` | `character varying(255)` | YES |  |  |
| `invoice_uuid` | `character varying(100)` | YES |  |  |
| `type` | `character varying(100)` | NO |  |  |
| `sub_total` | `numeric(15,2)` | YES |  |  |
| `tax_amount` | `numeric(15,2)` | YES |  |  |
| `total_amount` | `numeric(15,2)` | NO |  |  |
| `currency_code` | `character varying(100)` | YES |  |  |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `remarks` | `character varying(500)` | YES |  |  |
| `buyer_id` | `bigint(64,0)` | YES |  | FK → `public.buyer_information.id` |
| `supplier_id` | `bigint(64,0)` | YES |  | FK → `public.supplier_information.id` |
| `uuid` | `character varying(255)` | NO |  |  |
| `is_used` | `boolean` | YES | false |  |
| `requester_name` | `character varying(255)` | YES |  |  |
| `requester_uuid` | `character varying(255)` | YES |  |  |
| `approval_route_name` | `character varying(255)` | YES |  |  |
| `approval_route_sequence` | `text` | YES |  |  |
| `approval_route_uuid` | `character varying(255)` | YES |  |  |
| `next_approver` | `character varying(255)` | YES |  |  |
| `next_approval_group_uuid` | `character varying(255)` | YES |  |  |
| `cn_approval_date` | `timestamp with time zone` | YES |  |  |
| `project_code` | `character varying(50)` | YES |  |  |
| `ap_specialist_approved_uuid` | `character varying(100)` | YES |  |  |
| `aggregate_tax_amount` | `numeric(15,2)` | YES | 0 |  |
| `invoice_id` | `bigint(64,0)` | YES |  | FK → `public.invoice.id` |
| `total_amount_document_currency` | `numeric(15,2)` | YES | 0 |  |
| `pc_uuid` | `text` | YES |  |  |
| `invoice_nature` | `character varying(255)` | YES |  |  |

#### `public.credit_note_applied_in_financing`

- **Type:** BASE TABLE  **Rows:** 17

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO |  | PK |
| `cn_id` | `bigint(64,0)` | YES |  | FK → `public.credit_note.id` |
| `financing_no` | `character varying(255)` | YES |  |  |
| `financing_uuid` | `character varying(255)` | YES |  |  |
| `used_supplier_financing` | `boolean` | YES | false |  |

**Indexes:**
- `pk_credit_note_applied_in_financing`: `CREATE UNIQUE INDEX pk_credit_note_applied_in_financing ON public.credit_note_applied_in_financing USING btree (id)`

#### `public.credit_note_applied_in_payment`

- **Type:** BASE TABLE  **Rows:** 148

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO |  | PK |
| `cn_id` | `bigint(64,0)` | YES |  | FK → `public.credit_note.id` |
| `payment_no` | `character varying(255)` | YES |  |  |
| `payment_uuid` | `character varying(255)` | YES |  |  |

**Indexes:**
- `pk_credit_note_applied_in_payment`: `CREATE UNIQUE INDEX pk_credit_note_applied_in_payment ON public.credit_note_applied_in_payment USING btree (id)`

#### `public.credit_note_audit_trail`

- **Type:** BASE TABLE  **Rows:** 1857

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('credit_note_audit_trail_id_s... | PK |
| `user_uuid` | `character varying(50)` | NO |  |  |
| `user_name` | `character varying(100)` | NO |  |  |
| `role` | `character varying(50)` | YES |  |  |
| `action` | `character varying(255)` | NO |  |  |
| `created_date` | `timestamp with time zone` | NO | now() |  |
| `credit_note_id` | `bigint(64,0)` | YES |  | FK → `public.credit_note.id` |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |

#### `public.credit_note_details_view`

- **Type:** VIEW  **Rows:** —

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `documentnumber` | `character varying(50)` | YES |  |  |
| `batchdate` | `timestamp with time zone` | YES |  |  |
| `cn_approval_date` | `timestamp with time zone` | YES |  |  |
| `credit_note_number` | `character varying(50)` | YES |  |  |
| `remarks` | `character varying(500)` | YES |  |  |
| `description` | `text` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `creditnote_uuid` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `invoice_uuid` | `character varying(100)` | YES |  |  |
| `documenttype` | `text` | YES |  |  |
| `documentdate` | `timestamp with time zone` | YES |  |  |
| `documenttotalincludingtax` | `numeric(15,2)` | YES |  |  |
| `date` | `timestamp with time zone` | YES |  |  |
| `currency` | `character varying(100)` | YES |  |  |
| `sub_total` | `numeric(15,2)` | YES |  |  |
| `tax_amount` | `numeric(15,2)` | YES |  |  |
| `taxtype` | `integer(32,0)` | YES |  |  |
| `taxclass` | `integer(32,0)` | YES |  |  |
| `taxclass1` | `integer(32,0)` | YES |  |  |
| `taxgroup` | `text` | YES |  |  |
| `tax_base` | `numeric(15,2)` | YES |  |  |
| `total_amount` | `numeric(15,2)` | YES |  |  |
| `invoice_number` | `character varying(255)` | YES |  |  |
| `project_code` | `character varying(50)` | YES |  |  |
| `amtcost` | `numeric` | YES |  |  |
| `item_net_price` | `numeric(15,2)` | YES |  |  |
| `textdesc` | `text` | YES |  |  |
| `glacct` | `character varying(255)` | YES |  |  |
| `item` | `character varying(100)` | YES |  |  |
| `cost_code` | `character varying(255)` | YES |  |  |
| `uom` | `character varying(50)` | YES |  |  |
| `quantity` | `numeric` | YES |  |  |
| `tax_code` | `character varying(255)` | YES |  |  |
| `tax_percent` | `numeric` | YES |  |  |
| `invoicedescription` | `character varying(1000)` | YES |  |  |
| `duedate` | `timestamp with time zone` | YES |  |  |
| `project_title` | `character varying(1000)` | YES |  |  |
| `project` | `character varying(1000)` | YES |  |  |
| `ponumber` | `character varying(255)` | YES |  |  |
| `ordnumber` | `character varying(255)` | YES |  |  |
| `accountset` | `character varying(255)` | YES |  |  |
| `buyercode` | `character varying(255)` | YES |  |  |
| `vendornumber` | `character varying(255)` | YES |  |  |
| `supplier_company_name` | `character varying(255)` | YES |  |  |
| `supplier_uen` | `character varying(50)` | YES |  |  |
| `supplier_uuid` | `character varying(255)` | YES |  |  |
| `buyer_address_label` | `character varying(500)` | YES |  |  |
| `buyer_address_first_line` | `character varying(500)` | YES |  |  |
| `buyer_address_second_line` | `character varying(200)` | YES |  |  |
| `buyer_city` | `character varying(100)` | YES |  |  |
| `buyer_state` | `character varying(100)` | YES |  |  |
| `buyer_country` | `character varying(100)` | YES |  |  |
| `buyer_postal_code` | `character varying(20)` | YES |  |  |

#### `public.credit_note_document_metadata`

- **Type:** BASE TABLE  **Rows:** 14

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('credit_note_document_metadat... | PK |
| `guid` | `character varying(50)` | NO |  |  |
| `file_label` | `character varying(255)` | NO |  |  |
| `file_description` | `character varying(255)` | NO |  |  |
| `uploaded_on` | `timestamp with time zone` | NO | now() |  |
| `uploaded_by_name` | `character varying(100)` | NO |  |  |
| `uploaded_by_uuid` | `character varying(50)` | NO |  |  |
| `credit_note_id` | `bigint(64,0)` | YES |  | FK → `public.credit_note.id` |
| `external_document` | `boolean` | YES | false |  |
| `file_name` | `character varying(255)` | YES |  |  |

#### `public.credit_note_item`

- **Type:** BASE TABLE  **Rows:** 1553

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('credit_note_item_id_seq'::re... | PK |
| `item_description` | `text` | NO |  |  |
| `item_quantity` | `numeric` | YES |  |  |
| `unit_price` | `numeric` | YES |  |  |
| `tax_code` | `character varying(255)` | NO |  |  |
| `tax_percent` | `numeric` | YES |  |  |
| `gl_account_number` | `character varying(255)` | YES |  |  |
| `gl_account_uuid` | `character varying(255)` | YES |  |  |
| `notes` | `character varying(500)` | YES |  |  |
| `cn_item_uuid` | `character varying(255)` | YES |  |  |
| `credit_note_id` | `bigint(64,0)` | YES |  | FK → `public.credit_note.id` |
| `uom_code` | `character varying(50)` | YES |  |  |
| `inv_item_code` | `character varying(100)` | YES |  |  |
| `inv_item_description` | `text` | YES |  |  |
| `inv_item_model` | `character varying(255)` | YES |  |  |
| `inv_item_size` | `character varying(500)` | YES |  |  |
| `inv_item_brand` | `character varying(255)` | YES |  |  |
| `item_net_price` | `numeric(15,2)` | YES |  |  |
| `exchange_rate` | `numeric` | YES |  |  |
| `price_type` | `character varying(100)` | YES |  |  |
| `cost_code` | `character varying(255)` | YES |  |  |
| `department_code` | `character varying(255)` | YES |  |  |
| `cat_item_id` | `bigint(64,0)` | YES |  |  |
| `item_quantity_str` | `character varying(255)` | YES | ''::character varying |  |
| `unit_price_str` | `character varying(255)` | YES | ''::character varying |  |
| `exchange_rate_str` | `character varying(255)` | YES | ''::character varying |  |
| `item_category` | `character varying(100)` | YES |  |  |
| `item_category_uuid` | `character varying(255)` | YES |  |  |
| `tax_uuid` | `character varying` | YES |  |  |
| `uom_uuid` | `character varying(36)` | YES |  |  |
| `forecast_trade_uuid` | `character varying(255)` | YES |  |  |
| `forecast_trade_label` | `character varying(255)` | YES |  |  |
| `have_children` | `boolean` | YES | false |  |
| `parent_uuid` | `character varying(255)` | YES |  |  |
| `parent_id` | `bigint(64,0)` | YES |  | FK → `public.credit_note_item.id` |
| `item_serial_number` | `numeric(10,2)` | YES |  |  |
| `project_uuid` | `character varying(255)` | YES |  |  |
| `project_code` | `character varying(255)` | YES |  |  |
| `work_done_month` | `date` | YES |  |  |

#### `public.databasechangelog`

- **Type:** BASE TABLE  **Rows:** 40

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `character varying(255)` | NO |  |  |
| `author` | `character varying(255)` | NO |  |  |
| `filename` | `character varying(255)` | NO |  |  |
| `dateexecuted` | `timestamp without time zone` | NO |  |  |
| `orderexecuted` | `integer(32,0)` | NO |  |  |
| `exectype` | `character varying(10)` | NO |  |  |
| `md5sum` | `character varying(35)` | YES |  |  |
| `description` | `character varying(255)` | YES |  |  |
| `comments` | `character varying(255)` | YES |  |  |
| `tag` | `character varying(255)` | YES |  |  |
| `liquibase` | `character varying(20)` | YES |  |  |
| `contexts` | `character varying(255)` | YES |  |  |
| `labels` | `character varying(255)` | YES |  |  |
| `deployment_id` | `character varying(10)` | YES |  |  |

#### `public.databasechangeloglock`

- **Type:** BASE TABLE  **Rows:** 1

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO |  | PK |
| `locked` | `boolean` | NO |  |  |
| `lockgranted` | `timestamp without time zone` | YES |  |  |
| `lockedby` | `character varying(255)` | YES |  |  |

#### `public.debit_note`

- **Type:** BASE TABLE  **Rows:** 331

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('debit_note_id_seq'::regclass) | PK |
| `debit_note_number` | `character varying(50)` | NO |  |  |
| `global_dn_number` | `character varying(50)` | NO |  |  |
| `status` | `character varying(255)` | NO |  |  |
| `debit_note_date` | `timestamp with time zone` | NO |  |  |
| `submission_date` | `timestamp with time zone` | NO | now() |  |
| `invoice_number` | `character varying(255)` | YES |  |  |
| `invoice_uuid` | `character varying(100)` | YES |  |  |
| `type` | `character varying(100)` | NO |  |  |
| `sub_total` | `numeric(26,2)` | YES |  |  |
| `tax_amount` | `numeric(26,2)` | YES |  |  |
| `total_amount` | `numeric(26,2)` | NO |  |  |
| `currency_code` | `character varying(100)` | YES |  |  |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `remarks` | `character varying(500)` | YES |  |  |
| `buyer_id` | `bigint(64,0)` | YES |  | FK → `public.buyer_information.id` |
| `supplier_id` | `bigint(64,0)` | YES |  | FK → `public.supplier_information.id` |
| `uuid` | `character varying(255)` | NO |  |  |
| `is_used` | `boolean` | YES | false |  |
| `requester_name` | `character varying(255)` | YES |  |  |
| `requester_uuid` | `character varying(255)` | YES |  |  |
| `project_code` | `character varying(50)` | YES |  |  |
| `approval_route_name` | `character varying(255)` | YES |  |  |
| `approval_route_sequence` | `text` | YES |  |  |
| `approval_route_uuid` | `character varying(255)` | YES |  |  |
| `next_approver` | `character varying(255)` | YES |  |  |
| `next_approval_group_uuid` | `character varying(255)` | YES |  |  |
| `dn_approval_date` | `timestamp with time zone` | YES |  |  |
| `ap_specialist_approved_uuid` | `character varying(100)` | YES |  |  |
| `aggregate_tax_amount` | `numeric(26,2)` | YES | 0 |  |
| `paid_amount` | `numeric(15,2)` | YES | 0 |  |
| `processing_amt` | `numeric(15,2)` | YES | 0 |  |
| `payment_number` | `character varying(5000)` | YES |  |  |
| `payment_status` | `character varying(255)` | YES |  |  |
| `total_amount_document_currency` | `numeric(15,2)` | YES | 0 |  |
| `po_number` | `character varying(500)` | YES |  |  |
| `processing_payment_amt` | `numeric(25,12)` | YES | 0 |  |
| `paid_payment_amount` | `numeric(25,12)` | YES | 0 |  |
| `from_invoice_type` | `character varying(50)` | YES | 'PO_INVOICE'::character varying |  |
| `invoice_nature` | `character varying(255)` | YES |  |  |

#### `public.debit_note_applied_in_payment`

- **Type:** BASE TABLE  **Rows:** 38

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO |  | PK |
| `dn_id` | `bigint(64,0)` | YES |  | FK → `public.debit_note.id` |
| `payment_no` | `character varying(255)` | YES |  |  |
| `payment_uuid` | `character varying(255)` | YES |  |  |

**Indexes:**
- `pk_debit_note_applied_in_payment`: `CREATE UNIQUE INDEX pk_debit_note_applied_in_payment ON public.debit_note_applied_in_payment USING btree (id)`

#### `public.debit_note_audit_trail`

- **Type:** BASE TABLE  **Rows:** 610

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('debit_note_audit_trail_id_se... | PK |
| `user_uuid` | `character varying(50)` | NO |  |  |
| `user_name` | `character varying(100)` | NO |  |  |
| `role` | `character varying(50)` | YES |  |  |
| `action` | `character varying(255)` | NO |  |  |
| `created_date` | `timestamp with time zone` | NO | now() |  |
| `debit_note_id` | `bigint(64,0)` | YES |  | FK → `public.debit_note.id` |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |

#### `public.debit_note_document_metadata`

- **Type:** BASE TABLE  **Rows:** 0

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('debit_note_document_metadata... | PK |
| `guid` | `character varying(50)` | NO |  |  |
| `file_label` | `character varying(255)` | NO |  |  |
| `file_description` | `character varying(255)` | NO |  |  |
| `uploaded_on` | `timestamp with time zone` | NO | now() |  |
| `uploaded_by_name` | `character varying(100)` | NO |  |  |
| `uploaded_by_uuid` | `character varying(50)` | NO |  |  |
| `debit_note_id` | `bigint(64,0)` | YES |  | FK → `public.debit_note.id` |
| `external_document` | `boolean` | YES | false |  |
| `file_name` | `character varying(255)` | YES |  |  |

#### `public.debit_note_item`

- **Type:** BASE TABLE  **Rows:** 580

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('debit_note_item_id_seq'::reg... | PK |
| `item_description` | `text` | YES |  |  |
| `item_quantity` | `numeric(25,12)` | YES |  |  |
| `unit_price` | `numeric(25,12)` | YES |  |  |
| `tax_code` | `character varying(255)` | NO |  |  |
| `tax_percent` | `numeric(25,12)` | YES |  |  |
| `gl_account_number` | `character varying(255)` | YES |  |  |
| `gl_account_uuid` | `character varying(255)` | YES |  |  |
| `notes` | `character varying(500)` | YES |  |  |
| `dn_item_uuid` | `character varying(255)` | YES |  |  |
| `debit_note_id` | `bigint(64,0)` | YES |  | FK → `public.debit_note.id` |
| `uom_code` | `character varying(50)` | YES |  |  |
| `inv_item_code` | `character varying(100)` | YES |  |  |
| `inv_item_description` | `text` | YES |  |  |
| `inv_item_model` | `character varying(255)` | YES |  |  |
| `inv_item_size` | `character varying(500)` | YES |  |  |
| `inv_item_brand` | `character varying(255)` | YES |  |  |
| `exchange_rate` | `numeric(25,12)` | YES |  |  |
| `item_net_price` | `numeric(25,12)` | YES |  |  |
| `price_type` | `character varying(100)` | YES |  |  |
| `cost_code` | `character varying(255)` | YES |  |  |
| `department_code` | `character varying(255)` | YES |  |  |
| `cat_item_id` | `bigint(64,0)` | YES |  |  |
| `item_quantity_str` | `character varying(255)` | YES | ''::character varying |  |
| `unit_price_str` | `character varying(255)` | YES | ''::character varying |  |
| `exchange_rate_str` | `character varying(255)` | YES | ''::character varying |  |
| `item_category` | `character varying(100)` | YES |  |  |
| `item_category_uuid` | `character varying(255)` | YES |  |  |
| `tax_uuid` | `character varying` | YES |  |  |
| `uom_uuid` | `character varying(36)` | YES |  |  |
| `forecast_trade_uuid` | `character varying(255)` | YES |  |  |
| `forecast_trade_label` | `character varying(255)` | YES |  |  |
| `have_children` | `boolean` | YES | false |  |
| `parent_uuid` | `character varying(255)` | YES |  |  |
| `parent_id` | `bigint(64,0)` | YES |  | FK → `public.debit_note_item.id` |
| `item_serial_number` | `numeric(10,2)` | YES |  |  |
| `project_uuid` | `character varying(255)` | YES |  |  |
| `project_code` | `character varying(255)` | YES |  |  |

#### `public.debit_note_processing_amt`

- **Type:** BASE TABLE  **Rows:** 72

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO |  | PK |
| `debit_note_id` | `bigint(64,0)` | YES |  | FK → `public.debit_note.id` |
| `debit_note_uuid` | `character varying(255)` | YES |  |  |
| `payment_no` | `character varying(255)` | YES |  |  |
| `payment_ref` | `character varying(255)` | YES |  |  |
| `payment_uuid` | `character varying(255)` | YES |  |  |
| `payment_status` | `character varying(255)` | YES |  |  |
| `amount_to_pay` | `numeric(15,2)` | YES |  |  |
| `amount_from_cn` | `numeric(15,2)` | YES |  |  |

**Indexes:**
- `pk_debit_note_processing_amt`: `CREATE UNIQUE INDEX pk_debit_note_processing_amt ON public.debit_note_processing_amt USING btree (id)`

#### `public.dn_project_mapping`

- **Type:** BASE TABLE  **Rows:** 292

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('dn_project_mapping_id_seq'::... | PK |
| `debit_note_id` | `bigint(64,0)` | NO |  | FK → `public.debit_note.id` |
| `project_id` | `bigint(64,0)` | NO |  | FK → `public.project.id` |

#### `public.email_template`

- **Type:** BASE TABLE  **Rows:** 69

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('email_template_id_seq'::regc... | PK |
| `feature_code` | `character varying(50)` | YES |  |  |
| `action` | `character varying(50)` | YES |  |  |
| `subject` | `character varying(500)` | YES |  |  |
| `content` | `text` | YES |  |  |

**Indexes:**
- `email_template_id_uindex`: `CREATE UNIQUE INDEX email_template_id_uindex ON public.email_template USING btree (id)`
- `email_template_pk`: `CREATE UNIQUE INDEX email_template_pk ON public.email_template USING btree (id)`

#### `public.erp_api_configuration`

- **Type:** BASE TABLE  **Rows:** 48

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `company_uuid` | `character varying(100)` | NO |  |  |
| `api_type` | `character varying(250)` | NO |  |  |
| `api_url` | `character varying(250)` | NO |  |  |
| `user_name` | `character varying(100)` | YES |  |  |
| `password` | `character varying(100)` | YES |  |  |
| `id` | `integer(32,0)` | NO | nextval('erp_api_configuration_id_seq... |  |

**Indexes:**
- `erp_api_configuration_company_api_uindex`: `CREATE UNIQUE INDEX erp_api_configuration_company_api_uindex ON public.erp_api_configuration USING btree (company_uuid, api_type)`

#### `public.inv_bwh_debit_note`

- **Type:** BASE TABLE  **Rows:** 213

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('inv_bwh_debit_note_id_seq'::... | PK |
| `debit_note_uuid` | `character varying` | YES |  |  |
| `debit_note_number` | `character varying` | YES |  |  |
| `notes` | `character varying` | YES |  |  |
| `debit_note_date` | `timestamp without time zone` | YES |  |  |
| `invoice_id` | `bigint(64,0)` | YES |  | FK → `public.invoice.id` |

#### `public.inv_log_br_info`

- **Type:** BASE TABLE  **Rows:** 64

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('inv_log_br_info_id_seq'::reg... | PK |
| `invoice_id` | `bigint(64,0)` | YES |  |  |
| `original_br_uuid` | `character varying(255)` | YES |  |  |
| `uuid` | `character varying(255)` | YES |  |  |
| `br_number` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `project` | `boolean` | YES | false |  |
| `currency_code` | `character varying(255)` | YES |  |  |
| `total_amount` | `numeric(26,2)` | YES | 0.00 |  |
| `bl_no` | `character varying(255)` | YES |  |  |
| `bl_uuid` | `character varying(255)` | YES |  |  |
| `project_code` | `character varying(255)` | YES |  |  |

**Indexes:**
- `pk_inv_logistics_br_info`: `CREATE UNIQUE INDEX pk_inv_logistics_br_info ON public.inv_log_br_info USING btree (id)`

#### `public.inv_log_br_item`

- **Type:** BASE TABLE  **Rows:** 126

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('inv_log_br_item_id_seq'::reg... | PK |
| `item_name` | `character varying(255)` | YES |  |  |
| `original_item_uuid` | `character varying(255)` | YES |  |  |
| `ocean_freight` | `boolean` | YES |  |  |
| `uuid` | `character varying(255)` | YES |  |  |
| `actual_quantity` | `numeric(26,2)` | YES | 0.00 |  |
| `invoice_quantity` | `numeric(26,2)` | YES | 0.00 |  |
| `invoice_unit_price` | `numeric(26,2)` | YES | 0.00 |  |
| `invoice_net_price` | `numeric(26,2)` | YES | 0.00 |  |
| `invoice_tax_code` | `character varying(255)` | YES |  |  |
| `invoice_tax_rate` | `numeric(26,2)` | YES | 0.00 |  |
| `uom` | `character varying(255)` | YES |  |  |
| `unit_price` | `numeric(26,2)` | YES | 0.00 |  |
| `tax_code` | `character varying(255)` | YES |  |  |
| `tax_rate` | `numeric(26,2)` | YES | 0.00 |  |
| `booking_request_id` | `bigint(64,0)` | YES |  | FK → `public.inv_log_br_info.id` |
| `item_code` | `character varying(100)` | YES |  |  |
| `item_description` | `character varying(255)` | YES |  |  |
| `invoice_currency` | `character varying(255)` | YES |  |  |
| `br_item_currency` | `character varying(255)` | YES |  |  |
| `unit_price_in_selected_currency` | `numeric(26,2)` | YES | 0.00 |  |
| `net_price_in_selected_currency` | `numeric(26,2)` | YES | 0.00 |  |
| `tax_uuid` | `character varying` | YES |  |  |
| `invoice_tax_code_uuid` | `character varying` | YES |  |  |
| `uom_uuid` | `character varying` | YES |  |  |

**Indexes:**
- `pk_inv_log_br_item`: `CREATE UNIQUE INDEX pk_inv_log_br_item ON public.inv_log_br_item USING btree (id)`

#### `public.inv_log_manual_item`

- **Type:** BASE TABLE  **Rows:** 9

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('inv_log_manual_item_id_seq':... | PK |
| `item_name` | `character varying(255)` | YES |  |  |
| `invoice_quantity` | `numeric(26,2)` | YES | 0.00 |  |
| `invoice_unit_price` | `numeric(26,2)` | YES | 0.00 |  |
| `invoice_net_price` | `numeric(26,2)` | YES | 0.00 |  |
| `invoice_tax_code` | `character varying(255)` | YES |  |  |
| `invoice_tax_rate` | `numeric(26,2)` | YES | 0.00 |  |
| `invoice_id` | `bigint(64,0)` | YES |  | FK → `public.invoice.id` |
| `invoice_currency` | `character varying(255)` | YES |  |  |
| `unit_price_in_selected_currency` | `numeric(26,2)` | YES | 0.00 |  |
| `net_price_in_selected_currency` | `numeric(26,2)` | YES | 0.00 |  |
| `item_code` | `character varying(100)` | YES |  |  |
| `item_description` | `character varying(255)` | YES |  |  |
| `uom` | `character varying(255)` | YES |  |  |
| `invoice_tax_code_uuid` | `character varying` | YES |  |  |
| `uom_uuid` | `character varying(36)` | YES |  |  |

**Indexes:**
- `pk_inv_log_manual_item`: `CREATE UNIQUE INDEX pk_inv_log_manual_item ON public.inv_log_manual_item USING btree (id)`

#### `public.inv_pc_information`

- **Type:** BASE TABLE  **Rows:** 1624

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('inv_pc_information_id_seq'::... | PK |
| `invoice_id` | `bigint(64,0)` | NO |  | FK → `public.invoice.id` |
| `gl_code` | `character varying(255)` | YES |  |  |
| `cost_code` | `character varying(255)` | YES |  |  |
| `department_code` | `character varying(255)` | YES |  |  |
| `wo_uuid` | `character varying(255)` | YES |  |  |
| `latest_approved` | `boolean` | YES | false |  |
| `gl_description` | `character varying(255)` | YES |  |  |

#### `public.inv_pc_response`

- **Type:** BASE TABLE  **Rows:** 2726

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO |  | PK |
| `invoice_id` | `bigint(64,0)` | YES |  |  |
| `pc_uuid` | `character varying(255)` | YES |  |  |
| `pc_number` | `character varying(255)` | YES |  |  |
| `wo_uuid` | `character varying(255)` | YES |  |  |
| `wo_number` | `character varying(255)` | YES |  |  |
| `claim_start_date` | `timestamp without time zone` | YES |  |  |
| `claim_end_date` | `timestamp without time zone` | YES |  |  |
| `claim_date` | `timestamp without time zone` | YES |  |  |
| `pr_reference_number` | `character varying(255)` | YES |  |  |
| `pc_reference_number` | `character varying(255)` | YES |  |  |
| `response_date` | `timestamp without time zone` | YES |  |  |
| `cum_response_original_contract_amt` | `numeric` | YES | 0 |  |
| `response_materials_amt` | `numeric` | YES | 0 |  |
| `cum_response_variation_amt` | `numeric` | YES | 0 |  |
| `advance_payment_loan` | `numeric` | YES | 0 |  |
| `advance_payment_work_done` | `numeric` | YES | 0 |  |
| `deposit_rental` | `numeric` | YES | 0 |  |
| `deposit_others` | `numeric` | YES | 0 |  |
| `retention_release_pb` | `numeric` | YES | 0 |  |
| `retention_release_work_done` | `numeric` | YES | 0 |  |
| `subtotal_before_retention_adj` | `numeric` | YES | 0 |  |
| `subtotal_after_retention_adj` | `numeric` | YES | 0 |  |
| `final_retention` | `numeric` | YES | 0 |  |
| `pre_cum_payments` | `numeric` | YES | 0 |  |
| `subtotal_response_amt` | `numeric` | YES | 0 |  |
| `retention_others` | `numeric` | YES | 0 |  |
| `advance_payment_recovery_loan` | `numeric` | YES | 0 |  |
| `advance_payment_recovery_work_done` | `numeric` | YES | 0 |  |
| `deposit_refundable_rental` | `numeric` | YES | 0 |  |
| `deposit_refundable_others` | `numeric` | YES | 0 |  |
| `back_charge_amt` | `numeric` | YES | 0 |  |
| `balance_due` | `numeric` | YES | 0 |  |
| `contract_title` | `character varying(500)` | YES |  |  |
| `retention_cap` | `numeric` | YES | 0 |  |
| `retention_materials` | `numeric` | YES | 0 |  |
| `retention_work_done` | `numeric` | YES | 0 |  |
| `subtotal_response_amt_with_tax` | `numeric` | YES | 0 |  |
| `balance_due_with_tax` | `numeric` | YES | 0 |  |
| `tax_amt` | `numeric` | YES | 0 |  |
| `adjusted_tax_amount` | `numeric` | YES | 0 |  |
| `back_charge_deduction` | `numeric` | YES | 0 |  |
| `back_charge_refund` | `numeric` | YES | 0 |  |
| `retention_added_to_cap_subcon_vr` | `numeric` | YES | 0 |  |
| `claim_month` | `timestamp without time zone` | YES |  |  |
| `applicable_to_payment_retention` | `numeric(19,2)` | YES |  |  |
| `applicable_to_payment_bc_refund` | `numeric(19,2)` | YES |  |  |
| `applicable_to_payment_bc_deduction` | `numeric(19,2)` | YES |  |  |
| `applicable_to_payment_retention_release_pb` | `numeric(19,2)` | YES |  |  |

**Indexes:**
- `pk_inv_pc_response`: `CREATE UNIQUE INDEX pk_inv_pc_response ON public.inv_pc_response USING btree (id)`

#### `public.inv_pc_response_tax`

- **Type:** BASE TABLE  **Rows:** 16796

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO |  | PK |
| `description` | `character varying(255)` | YES |  |  |
| `gst_available` | `boolean` | YES |  |  |
| `tax_code` | `character varying(255)` | YES |  |  |
| `tax_rate` | `numeric` | YES | 0 |  |
| `pc_response_id` | `bigint(64,0)` | YES |  | FK → `public.inv_pc_response.id` |
| `tax_amt` | `numeric` | YES | 0 |  |

**Indexes:**
- `pk_inv_pc_response_tax`: `CREATE UNIQUE INDEX pk_inv_pc_response_tax ON public.inv_pc_response_tax USING btree (id)`

#### `public.inv_project_mapping`

- **Type:** BASE TABLE  **Rows:** 7044

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('inv_project_mapping_id_seq':... | PK |
| `invoice_id` | `bigint(64,0)` | NO |  | FK → `public.invoice.id` |
| `project_id` | `bigint(64,0)` | NO |  | FK → `public.project.id` |

#### `public.invoice`

- **Type:** BASE TABLE  **Rows:** 9289

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('invoice_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `invoice_no` | `character varying(255)` | YES |  |  |
| `invoice_global_no` | `character varying(255)` | YES |  |  |
| `invoice_type` | `character varying(255)` | YES |  |  |
| `invoice_status` | `character varying(255)` | YES |  |  |
| `matching` | `character varying(255)` | YES |  |  |
| `payment_status` | `character varying(255)` | YES |  |  |
| `two_way_matching` | `boolean` | YES |  |  |
| `currency_code` | `character varying(100)` | YES |  |  |
| `sub_total` | `numeric(15,2)` | YES |  |  |
| `tax` | `numeric` | YES |  |  |
| `total_amount` | `numeric(15,2)` | YES |  |  |
| `paid_amount` | `numeric(15,2)` | YES |  |  |
| `expected_amount` | `numeric(15,2)` | YES |  |  |
| `expected_amount_given` | `boolean` | YES |  |  |
| `invoice_submission_date` | `timestamp with time zone` | YES | now() |  |
| `payment_terms` | `character varying(255)` | YES |  |  |
| `invoice_due_date` | `timestamp with time zone` | YES | now() |  |
| `invoice_approval_date` | `timestamp with time zone` | YES | now() |  |
| `invoice_date` | `timestamp with time zone` | YES | now() |  |
| `submitted_by` | `character varying(255)` | YES |  |  |
| `submitted_staff` | `character varying(255)` | YES |  |  |
| `buyer_id` | `bigint(64,0)` | YES |  | FK → `public.buyer_information.id` |
| `supplier_id` | `bigint(64,0)` | YES |  | FK → `public.supplier_information.id` |
| `approval_route_name` | `character varying(255)` | YES |  |  |
| `approval_route_sequence` | `text` | YES |  |  |
| `approval_route_uuid` | `character varying(255)` | YES |  |  |
| `next_approver` | `character varying(255)` | YES |  |  |
| `next_approval_group_uuid` | `character varying(255)` | YES |  |  |
| `project_code` | `character varying(50)` | YES |  |  |
| `project_code_uuid` | `character varying(50)` | YES |  |  |
| `project_title` | `character varying(1000)` | YES |  |  |
| `exchange_rate` | `numeric` | YES |  |  |
| `pending_payment_approval_amt` | `numeric(15,2)` | YES | 0 |  |
| `payment_number` | `character varying(5000)` | YES |  |  |
| `currency_name` | `character varying(255)` | YES |  |  |
| `processing_payment_amt` | `numeric(15,2)` | YES | 0 |  |
| `tmp_payment_status` | `character varying(255)` | YES | 'NOT_PAID'::character varying |  |
| `invoice_nature` | `character varying(25)` | YES |  |  |
| `payment_terms_days` | `integer(32,0)` | YES | 0 |  |
| `aggregate_tax_amount` | `numeric(15,2)` | YES | 0 |  |
| `has_reissued` | `boolean` | YES | false |  |
| `processing_amt` | `numeric(15,2)` | YES | 0 |  |
| `processing_financing_amt` | `numeric(15,2)` | YES | 0 |  |
| `paid_financing_amount` | `numeric(15,2)` | YES | 0 |  |
| `paid_payment_amount` | `numeric(15,2)` | YES | 0 |  |
| `payment_notes` | `character varying(500)` | YES |  |  |
| `updated_at` | `timestamp with time zone` | YES | now() |  |
| `br_quantity` | `integer(32,0)` | YES | 0 |  |
| `reissued_invoice_uuid` | `character varying(255)` | YES |  |  |
| `fixed_amount_discount` | `numeric(26,2)` | YES | 0 |  |
| `percentage_discount` | `numeric(26,2)` | YES | 0 |  |
| `is_discount_applied` | `boolean` | YES | false |  |
| `requester_uuid` | `character varying(255)` | YES |  |  |
| `root_uuids` | `text` | YES |  |  |
| `payment_inv_due_date` | `timestamp with time zone` | YES | now() |  |
| `payment_terms_uuid` | `character varying(36)` | YES |  |  |
| `remarks` | `text` | YES |  |  |
| `transaction_type_code` | `character varying(255)` | YES |  |  |
| `transaction_type_name` | `character varying(255)` | YES |  |  |
| `transaction_type_uuid` | `character varying(255)` | YES |  |  |
| `reason` | `character varying(255)` | YES |  |  |
| `latest_payment_date` | `timestamp without time zone` | YES |  |  |

**Indexes:**
- `uk_invoice_no_buyer_supplier_requester`: `CREATE UNIQUE INDEX uk_invoice_no_buyer_supplier_requester ON public.invoice USING btree (invoice_no, buyer_id, supplier_id, requester_uuid)`

#### `public.invoice_audit_trail`

- **Type:** BASE TABLE  **Rows:** 21236

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('invoice_audit_trail_id_seq':... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `role` | `character varying(255)` | YES |  |  |
| `action` | `character varying(255)` | YES |  |  |
| `invoice_status` | `character varying(255)` | YES |  |  |
| `date` | `timestamp with time zone` | YES | now() |  |
| `invoice_id` | `bigint(64,0)` | YES |  | FK → `public.invoice.id` |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `payment_batch_uuid` | `character varying(255)` | YES |  |  |
| `payment_batch_no` | `character varying(255)` | YES |  |  |
| `payment_batch_amount` | `numeric(19,2)` | YES |  |  |

#### `public.invoice_details_view`

- **Type:** VIEW  **Rows:** —

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `documentnumber` | `character varying(255)` | YES |  |  |
| `batchdate` | `timestamp with time zone` | YES |  |  |
| `description` | `text` | YES |  |  |
| `invoice_status` | `character varying(255)` | YES |  |  |
| `invoice_approval_date` | `timestamp with time zone` | YES |  |  |
| `invoiceuuid` | `character varying(255)` | YES |  |  |
| `project_title` | `character varying(1000)` | YES |  |  |
| `documenttype` | `text` | YES |  |  |
| `invoicedescription` | `character varying(1000)` | YES |  |  |
| `duedate` | `timestamp with time zone` | YES |  |  |
| `documentdate` | `timestamp with time zone` | YES |  |  |
| `documenttotalincludingtax` | `numeric(15,2)` | YES |  |  |
| `taxbase` | `numeric(15,2)` | YES |  |  |
| `taxtype` | `integer(32,0)` | YES |  |  |
| `taxclass` | `integer(32,0)` | YES |  |  |
| `taxamt` | `numeric` | YES |  |  |
| `tax` | `numeric` | YES |  |  |
| `taxgroup` | `text` | YES |  |  |
| `project` | `character varying(50)` | YES |  |  |
| `invoice_type` | `character varying(255)` | YES |  |  |
| `currency` | `character varying(100)` | YES |  |  |
| `project_code` | `character varying(50)` | YES |  |  |
| `sub_total` | `numeric(15,2)` | YES |  |  |
| `netinvamt` | `numeric(15,2)` | YES |  |  |
| `totaltax` | `numeric` | YES |  |  |
| `payment_term` | `character varying(255)` | YES |  |  |
| `ordnumber` | `character varying(255)` | YES |  |  |
| `ponumber` | `character varying(255)` | YES |  |  |
| `item` | `character varying(100)` | YES |  |  |
| `resource` | `character varying(255)` | YES |  |  |
| `category` | `character varying(100)` | YES |  |  |
| `uom` | `character varying(255)` | YES |  |  |
| `do_number` | `character varying(255)` | YES |  |  |
| `qtyinvc` | `numeric` | YES |  |  |
| `amtcost` | `numeric` | YES |  |  |
| `unitcost` | `numeric` | YES |  |  |
| `invoice_unit_price` | `numeric` | YES |  |  |
| `invoice_net_price` | `numeric(15,2)` | YES |  |  |
| `billrate` | `numeric` | YES |  |  |
| `billtype` | `text` | YES |  |  |
| `textdesc` | `text` | YES |  |  |
| `comment` | `character varying(500)` | YES |  |  |
| `tax_code` | `character varying(100)` | YES |  |  |
| `taxpercentage` | `numeric` | YES |  |  |
| `invoicenetprice` | `numeric(15,2)` | YES |  |  |
| `glcode` | `character varying(255)` | YES |  |  |
| `cost_code` | `character varying(255)` | YES |  |  |
| `tax_claimable` | `boolean` | YES |  |  |
| `invoice_tax_amount` | `numeric(15,2)` | YES |  |  |
| `buyercode` | `character varying(255)` | YES |  |  |
| `company_name` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(100)` | YES |  |  |
| `accountset` | `character varying(255)` | YES |  |  |
| `vendornumber` | `character varying(255)` | YES |  |  |
| `supplier_code` | `character varying(255)` | YES |  |  |
| `supplier_company_name` | `character varying(255)` | YES |  |  |
| `supplier_uen` | `character varying(50)` | YES |  |  |
| `supplier_uuid` | `character varying(255)` | YES |  |  |
| `buyer_address_label` | `character varying(500)` | YES |  |  |
| `buyer_address_first_line` | `character varying(500)` | YES |  |  |
| `buyer_address_second_line` | `character varying(200)` | YES |  |  |
| `buyer_city` | `character varying(100)` | YES |  |  |
| `buyer_state` | `character varying(100)` | YES |  |  |
| `buyer_country` | `character varying(100)` | YES |  |  |
| `buyer_postal_code` | `character varying(20)` | YES |  |  |
| `contract` | `text` | YES |  |  |

#### `public.invoice_document_metadata`

- **Type:** BASE TABLE  **Rows:** 231

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('invoice_document_metadata_id... | PK |
| `guid` | `character varying(50)` | YES |  |  |
| `file_label` | `character varying(255)` | YES |  |  |
| `file_description` | `character varying(255)` | YES |  |  |
| `uploaded_on` | `timestamp with time zone` | NO | now() |  |
| `uploaded_by` | `character varying(100)` | YES |  |  |
| `uploader_uuid` | `character varying(50)` | YES |  |  |
| `external_document` | `boolean` | YES |  |  |
| `invoice_id` | `bigint(64,0)` | YES |  | FK → `public.invoice.id` |
| `file_name` | `character varying(255)` | YES |  |  |

**Indexes:**
- `invoice_document_metadata_invoice_id_index`: `CREATE INDEX invoice_document_metadata_invoice_id_index ON public.invoice_document_metadata USING btree (invoice_id)`

#### `public.invoice_financing_processing_amt`

- **Type:** BASE TABLE  **Rows:** 363

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO |  | PK |
| `invoice_id` | `bigint(64,0)` | YES |  | FK → `public.invoice.id` |
| `invoice_uuid` | `character varying(255)` | YES |  |  |
| `financing_no` | `character varying(255)` | YES |  |  |
| `financing_uuid` | `character varying(255)` | YES |  |  |
| `action` | `character varying(255)` | YES |  |  |
| `amount_to_pay` | `numeric(15,2)` | YES |  |  |
| `used_supplier_financing` | `boolean` | YES | false |  |

**Indexes:**
- `pk_invoice_financing_processing_amt`: `CREATE UNIQUE INDEX pk_invoice_financing_processing_amt ON public.invoice_financing_processing_amt USING btree (id)`

#### `public.invoice_item`

- **Type:** BASE TABLE  **Rows:** 12475

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('invoice_item_id_seq'::regclass) | PK |
| `item_code` | `character varying(100)` | YES |  |  |
| `item_name` | `character varying(255)` | YES |  |  |
| `item_description` | `text` | YES |  |  |
| `model` | `character varying(255)` | YES |  |  |
| `size` | `character varying(500)` | YES |  |  |
| `brand` | `character varying(255)` | YES |  |  |
| `uom` | `character varying(255)` | YES |  |  |
| `notes` | `character varying(500)` | YES |  |  |
| `invoice_qty` | `numeric` | YES | 0 |  |
| `invoice_cumulative_qty` | `numeric` | YES | 0 |  |
| `invoice_unit_price` | `numeric` | YES |  |  |
| `invoice_tax_code` | `character varying(100)` | YES |  |  |
| `invoice_tax_code_uuid` | `character varying(255)` | YES |  |  |
| `invoice_tax_amount` | `numeric(15,2)` | YES |  |  |
| `po_number` | `character varying(255)` | YES |  |  |
| `po_uuid` | `character varying(255)` | YES |  |  |
| `po_qty` | `numeric` | YES | 0 |  |
| `po_unit_price` | `numeric` | YES |  |  |
| `po_tax_code` | `character varying(255)` | YES |  |  |
| `po_tax_code_uuid` | `character varying(255)` | YES |  |  |
| `reference_number` | `character varying(255)` | YES |  |  |
| `gl_code` | `character varying(255)` | YES |  |  |
| `do_number` | `character varying(255)` | YES |  |  |
| `do_uuid` | `character varying(255)` | YES |  |  |
| `gr_number` | `character varying(255)` | YES |  |  |
| `gr_uuid` | `character varying(255)` | YES |  |  |
| `do_qty_converted` | `numeric` | YES | 0 |  |
| `gr_qty_received` | `numeric` | YES | 0 |  |
| `gr_qty_rejected` | `numeric` | YES | 0 |  |
| `do_qty_received` | `numeric` | YES | 0 |  |
| `do_qty_rejected` | `numeric` | YES | 0 |  |
| `invoice_id` | `bigint(64,0)` | YES |  | FK → `public.invoice.id` |
| `invoice_net_price` | `numeric(15,2)` | YES |  |  |
| `invoice_tax_code_value` | `numeric` | YES |  |  |
| `po_tax_code_value` | `numeric` | YES |  |  |
| `pending_invoice_qty` | `numeric` | YES | 0 |  |
| `pending_invoice_net_price` | `numeric(15,2)` | YES |  |  |
| `po_net_price` | `numeric(15,2)` | YES |  |  |
| `invoice_net_rounded` | `numeric(15,2)` | YES | 0 |  |
| `invoice_net_rounded_dec_place` | `bigint(64,0)` | YES |  |  |
| `invoice_net_rounded_type` | `character varying(10)` | YES |  |  |
| `price_type` | `character varying(100)` | YES |  |  |
| `project_forecast_trade_code` | `character varying(50)` | YES |  |  |
| `item_category` | `character varying(100)` | YES |  |  |
| `item_category_uuid` | `character varying(255)` | YES |  |  |
| `cost_code` | `character varying(255)` | YES |  |  |
| `department_code` | `character varying(255)` | YES |  |  |
| `tax_claimable` | `boolean` | NO | true |  |
| `cat_item_id` | `bigint(64,0)` | YES |  |  |
| `po_item_id` | `bigint(64,0)` | YES |  |  |
| `do_item_id` | `bigint(64,0)` | YES |  |  |
| `discount_amount` | `numeric(26,2)` | YES | 0 |  |
| `po_discount_amount` | `numeric(26,2)` | YES | 0 |  |
| `invoice_qty_str` | `character varying(255)` | YES | ''::character varying |  |
| `invoice_unit_price_str` | `character varying(255)` | YES | ''::character varying |  |
| `po_qty_str` | `character varying(255)` | YES | ''::character varying |  |
| `po_unit_price_str` | `character varying(255)` | YES | ''::character varying |  |
| `contracted_price` | `numeric` | YES | 0 |  |
| `contracted` | `boolean` | YES | false |  |
| `contracted_price_str` | `character varying(255)` | YES | NULL::character varying |  |
| `gl_description` | `character varying(255)` | YES |  |  |
| `forecast_trade_uuid` | `character varying(255)` | YES |  |  |
| `forecast_trade_label` | `character varying(255)` | YES |  |  |
| `uom_uuid` | `character varying(36)` | YES |  |  |
| `cost_code_remark` | `character varying(255)` | YES |  |  |
| `department_code_remark` | `character varying(255)` | YES |  |  |
| `uuid` | `character varying(255)` | YES |  |  |
| `project_code` | `character varying(255)` | YES |  |  |
| `have_children` | `boolean` | YES | false |  |
| `parent_uuid` | `character varying(255)` | YES |  |  |
| `parent_id` | `bigint(64,0)` | YES |  | FK → `public.invoice_item.id` |
| `project_uuid` | `character varying(255)` | YES |  |  |
| `item_serial_number` | `numeric(10,2)` | YES |  |  |
| `transaction_type_uuid` | `character varying(255)` | YES |  |  |
| `transaction_type_code` | `character varying(255)` | YES |  |  |
| `transaction_type_name` | `character varying(255)` | YES |  |  |
| `work_done_month` | `date` | YES |  |  |
| `serial_number` | `bigint(64,0)` | YES |  |  |

#### `public.invoice_payment_details_view`

- **Type:** VIEW  **Rows:** —

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `vendornumber` | `character varying(255)` | YES |  |  |
| `invoiceuuid` | `character varying(255)` | YES |  |  |
| `documentnumber` | `character varying(255)` | YES |  |  |
| `paymentamount` | `numeric(15,2)` | YES |  |  |
| `payment_number` | `character varying(5000)` | YES |  |  |
| `accountset` | `character varying(255)` | YES |  |  |

#### `public.invoice_processing_amt`

- **Type:** BASE TABLE  **Rows:** 2918

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO |  | PK |
| `invoice_id` | `bigint(64,0)` | YES |  | FK → `public.invoice.id` |
| `invoice_uuid` | `character varying(255)` | YES |  |  |
| `payment_no` | `character varying(255)` | YES |  |  |
| `payment_ref` | `character varying(255)` | YES |  |  |
| `payment_uuid` | `character varying(255)` | YES |  |  |
| `payment_status` | `character varying(255)` | YES |  |  |
| `amount_to_pay` | `numeric(15,2)` | YES |  |  |
| `amount_from_cn` | `numeric(15,2)` | YES |  |  |
| `total_batch_amount` | `numeric(25,2)` | YES | 0 |  |
| `payment_release_date` | `timestamp without time zone` | YES |  |  |
| `executed_date` | `timestamp without time zone` | YES |  |  |

**Indexes:**
- `pk_invoice_processing_amt`: `CREATE UNIQUE INDEX pk_invoice_processing_amt ON public.invoice_processing_amt USING btree (id)`

#### `public.liquibase-changelog`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `character varying(255)` | NO |  |  |
| `author` | `character varying(255)` | NO |  |  |
| `filename` | `character varying(255)` | NO |  |  |
| `dateexecuted` | `timestamp without time zone` | NO |  |  |
| `orderexecuted` | `integer(32,0)` | NO |  |  |
| `exectype` | `character varying(10)` | NO |  |  |
| `md5sum` | `character varying(35)` | YES |  |  |
| `description` | `character varying(255)` | YES |  |  |
| `comments` | `character varying(255)` | YES |  |  |
| `tag` | `character varying(255)` | YES |  |  |
| `liquibase` | `character varying(20)` | YES |  |  |
| `contexts` | `character varying(255)` | YES |  |  |
| `labels` | `character varying(255)` | YES |  |  |
| `deployment_id` | `character varying(10)` | YES |  |  |

#### `public.liquibase-lock`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO |  | PK |
| `locked` | `boolean` | NO |  |  |
| `lockgranted` | `timestamp without time zone` | YES |  |  |
| `lockedby` | `character varying(255)` | YES |  |  |

**Indexes:**
- `LIQUIBASE-LOCK_PKEY`: `CREATE UNIQUE INDEX "LIQUIBASE-LOCK_PKEY" ON public."liquibase-lock" USING btree (id)`

#### `public.non_supplier`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('non_supplier_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `company_name` | `character varying(255)` | YES |  |  |
| `address_label` | `character varying(255)` | YES |  |  |
| `address_first_line` | `character varying(255)` | YES |  |  |
| `address_second_line` | `character varying(255)` | YES |  |  |
| `city` | `character varying(255)` | YES |  |  |
| `state` | `character varying(255)` | YES |  |  |
| `country` | `character varying(255)` | YES |  |  |
| `postal_code` | `character varying(50)` | YES |  |  |

#### `public.project`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('project_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `project_code` | `character varying(255)` | YES |  |  |
| `project_title` | `character varying(255)` | YES |  |  |
| `erp_project_code` | `character varying(255)` | YES |  |  |

#### `public.public_holidays`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('public_holidays_id_seq'::reg... | PK |
| `holiday_name` | `character varying(255)` | NO |  |  |
| `holiday_date` | `date` | NO |  |  |
| `is_active` | `boolean` | YES | true |  |

**Indexes:**
- `public_holidays_holiday_date_key`: `CREATE UNIQUE INDEX public_holidays_holiday_date_key ON public.public_holidays USING btree (holiday_date)`

#### `public.sequence_generator`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('sequence_generator_id_seq'::... | PK |
| `company_uuid` | `character varying(50)` | YES |  |  |
| `type` | `character varying(50)` | NO |  |  |
| `number` | `character varying(50)` | NO |  |  |

**Indexes:**
- `uq_company_uuid_type`: `CREATE UNIQUE INDEX uq_company_uuid_type ON public.sequence_generator USING btree (company_uuid, type)`

#### `public.supplier_information`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('supplier_information_id_seq'... | PK |
| `supplier_code` | `character varying(255)` | YES |  |  |
| `supplier_uuid` | `character varying(255)` | YES |  |  |
| `company_name` | `character varying(255)` | YES |  |  |
| `supplier_company_uuid` | `character varying(100)` | YES |  |  |
| `gst_no` | `character varying(50)` | YES |  |  |
| `uen` | `character varying(50)` | YES |  |  |
| `md5check_sum` | `character varying(500)` | YES |  |  |
| `address_id` | `bigint(64,0)` | YES |  | FK → `public.addresses.id` |
| `country_of_origin` | `character varying(255)` | YES |  |  |
| `contact_person_id` | `bigint(64,0)` | YES |  | FK → `public.contact_person.id` |

#### `public.va_allocation_tracker`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('va_allocation_tracker_id_seq... | PK |
| `virtual_account_id` | `bigint(64,0)` | NO |  | FK → `public.virtual_account.id` |
| `allocation_type` | `character varying(50)` | NO |  |  |
| `document_type` | `character varying(50)` | NO |  |  |
| `allocator_name` | `character varying(255)` | YES |  |  |
| `pc_uuid` | `character varying(255)` | YES |  |  |
| `pc_number` | `character varying(255)` | NO |  |  |
| `claim_amt` | `numeric(19,2)` | NO |  |  |
| `inv_uuid` | `character varying(255)` | YES |  |  |
| `inv_no` | `character varying(255)` | YES |  |  |
| `inv_amt` | `numeric(19,2)` | YES |  |  |
| `va_allocated_amt` | `numeric(19,2)` | YES |  |  |

#### `public.virtual_account`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('virtual_card_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `number` | `character varying(20)` | NO | "left"(md5((random())::text), 16) |  |
| `holder_name` | `character varying(250)` | NO |  |  |
| `status` | `character varying(255)` | NO |  |  |
| `cvv` | `integer(32,0)` | YES |  |  |
| `card_balance` | `numeric(10,2)` | YES |  |  |
| `supplier_company_uuid` | `character varying(255)` | YES |  |  |
| `issued_date` | `timestamp with time zone` | NO | now() |  |
| `card_limit` | `numeric(10,2)` | YES |  |  |
| `root_wr_uuid` | `character varying(255)` | YES |  |  |
| `wr_uuid` | `character varying(255)` | YES |  |  |
| `primary_card_uuid` | `character varying(255)` | YES |  |  |
| `project_uuid` | `character varying(255)` | YES |  |  |
| `invoice_id` | `bigint(64,0)` | YES |  | FK → `public.invoice.id` |
| `type` | `character varying(50)` | YES |  |  |
| `processing_amt` | `numeric(15,2)` | YES | 0 |  |
| `adjusted_amt` | `numeric(12,2)` | YES | 0.00 |  |
| `pc_uuid` | `text` | YES |  |  |
| `ref_number` | `character varying` | YES |  |  |
| `pymt_processing_amt` | `numeric(19,2)` | NO | 0.00 |  |
| `inv_paid_amt_post_va` | `numeric(19,2)` | NO | 0.00 |  |
| `inv_unpaid_amt_at_va_creation` | `numeric(19,2)` | YES |  |  |
| `withdrawal_amt` | `numeric(19,2)` | NO | 0.00 |  |
| `va_branch_limit` | `numeric(19,2)` | YES |  |  |
| `active_date` | `timestamp without time zone` | YES |  |  |
| `regenerated_count` | `bigint(64,0)` | YES | 1 |  |
| `is_latest` | `boolean` | YES | true |  |
| `is_deactivated` | `boolean` | YES | false |  |
| `remark` | `text` | YES | ''::text |  |
| `fi_uuid` | `character varying(255)` | YES |  |  |
| `fi_name` | `character varying(255)` | YES |  |  |
| `expiration_date` | `character varying(20)` | YES |  |  |

#### `public.virtual_account_audit`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('virtual_account_audit_id_seq... | PK |
| `va_id` | `bigint(64,0)` | YES |  |  |
| `action` | `character varying(255)` | YES |  |  |
| `executed_date` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |
| `va_uuid` | `character varying(255)` | YES |  |  |
| `va_pc_uuid` | `character varying(255)` | YES |  |  |
| `is_deactivated` | `boolean` | YES |  |  |
| `va_status` | `character varying(50)` | YES |  |  |
| `regenerated_count` | `bigint(64,0)` | YES |  |  |
| `reason` | `character varying(255)` | YES |  |  |

#### `public.withdrawal`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('withdrawal_id_seq'::regclass) | PK |
| `uuid` | `text` | YES |  |  |
| `project_uuid` | `text` | NO |  |  |
| `supplier_bank_uuid` | `text` | YES |  |  |
| `supplier_company_uuid` | `text` | NO |  |  |
| `drawdown_description` | `text` | YES |  |  |
| `execution_date` | `timestamp with time zone` | YES |  |  |
| `issued_date` | `timestamp with time zone` | NO | now() |  |
| `drawdown_amount` | `text` | YES |  |  |
| `terms_conditions` | `boolean` | YES |  |  |
| `status` | `text` | YES |  |  |
| `bpsp_ref_code` | `text` | YES |  |  |
| `draw_down_type` | `text` | YES |  |  |
| `virtual_card_id` | `bigint(64,0)` | YES |  | FK → `public.virtual_account.id` |
| `invoice_id` | `bigint(64,0)` | YES |  | FK → `public.invoice.id` |
| `dtf_fee` | `text` | YES |  |  |
| `request_id` | `text` | YES |  |  |
| `received_amt` | `numeric(12,2)` | YES | 0.0 |  |
| `interest_rate` | `double precision` | YES | 0.0 |  |
| `fi_start_date` | `timestamp without time zone` | YES |  |  |
| `finance_principal` | `numeric(12,2)` | YES | 0.0 |  |
| `reason` | `character varying(255)` | YES |  |  |
| `approval_route_name` | `character varying(255)` | YES |  |  |
| `approval_route_sequence` | `character varying(255)` | YES |  |  |
| `approval_route_uuid` | `character varying(255)` | YES |  |  |
| `next_approver` | `character varying(255)` | YES |  |  |
| `next_approval_group_uuid` | `character varying(255)` | YES |  |  |
| `approval_date` | `timestamp with time zone` | YES |  |  |
| `ack_date` | `date` | YES |  |  |
| `platform_fee` | `text` | YES |  |  |

#### `public.withdrawal_audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('withdrawal_audit_trail_id_se... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `action` | `character varying(255)` | YES |  |  |
| `role` | `character varying(255)` | YES |  |  |
| `date` | `timestamp without time zone` | YES |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `withdrawal_status` | `character varying(255)` | YES |  |  |
| `withdrawal_id` | `bigint(64,0)` | NO |  |  |

#### `public.withdrawal_pdf_documents`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('withdrawal_pdf_documents_id_... | PK |
| `file_description` | `character varying(255)` | YES |  |  |
| `file_label` | `character varying(255)` | YES |  |  |
| `guid` | `character varying(255)` | YES |  |  |
| `remarks` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `type` | `character varying(255)` | YES |  |  |
| `withdrawal_id` | `bigint(64,0)` | YES |  | FK → `public.withdrawal.id` |

---

## logistics 1

**Schemas:** public
**Total tables:** 64

### Schema: `public`

#### `public.address`

- **Type:** BASE TABLE  **Rows:** 895

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('address_id_seq'::regclass) | PK |
| `uuid` | `character varying(36)` | NO |  |  |
| `address_label` | `character varying(255)` | YES |  |  |
| `address_first_line` | `character varying(255)` | NO |  |  |
| `address_second_line` | `character varying(255)` | YES |  |  |
| `city` | `character varying(100)` | YES |  |  |
| `state` | `character varying(100)` | NO |  |  |
| `country` | `character varying(100)` | NO |  |  |
| `postal_code` | `character varying(20)` | NO |  |  |

#### `public.bc_audit_trail`

- **Type:** BASE TABLE  **Rows:** 415

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('bc_audit_trail_id_seq'::regc... | PK |
| `action` | `character varying(255)` | YES |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `date_time` | `timestamp with time zone` | NO |  |  |
| `designation` | `character varying(255)` | YES |  |  |
| `remark` | `text` | YES |  |  |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `booking_confirmation_id` | `bigint(64,0)` | YES |  | FK → `public.booking_confirmation.id` |
| `pdf_version` | `character varying(255)` | YES |  |  |

#### `public.bc_document`

- **Type:** BASE TABLE  **Rows:** 10

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('bc_document_id_seq'::regclass) | PK |
| `description` | `character varying(500)` | YES |  |  |
| `external` | `boolean` | YES | false |  |
| `guid` | `character varying(255)` | YES |  |  |
| `label` | `character varying(255)` | YES |  |  |
| `name` | `character varying(255)` | YES |  |  |
| `uploaded_by` | `character varying(255)` | YES |  |  |
| `uploaded_on` | `character varying(255)` | YES |  |  |
| `uploader_uuid` | `character varying(255)` | YES |  |  |
| `booking_confirmation_id` | `bigint(64,0)` | YES |  | FK → `public.booking_confirmation.id` |

#### `public.booking_confirmation`

- **Type:** BASE TABLE  **Rows:** 135

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('booking_confirmation_id_seq'... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `cy_closing_at` | `timestamp with time zone` | YES |  |  |
| `updated_at` | `timestamp with time zone` | NO |  |  |
| `converted_at` | `timestamp with time zone` | YES |  |  |
| `booking_date` | `timestamp with time zone` | YES |  |  |
| `number` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `title` | `character varying(255)` | YES |  |  |
| `remarks` | `character varying(1000)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `requester_uuid` | `character varying(255)` | YES |  |  |
| `requester_name` | `character varying(255)` | YES |  |  |
| `master_ref` | `character varying(255)` | YES |  |  |
| `booking_ref` | `character varying(255)` | YES |  |  |
| `portnet_ref` | `character varying(255)` | YES |  |  |
| `payment_term` | `character varying(255)` | YES |  |  |
| `shipper` | `character varying(255)` | YES |  |  |
| `currency_code` | `character varying(255)` | YES |  |  |
| `currency_name` | `character varying(255)` | YES |  |  |
| `cc` | `character varying(255)` | YES |  |  |
| `number_of_package` | `double precision` | YES |  |  |
| `uom` | `character varying(255)` | YES |  |  |
| `total_weight` | `double precision` | YES |  |  |
| `package_type` | `character varying(255)` | YES |  |  |
| `total_measurement` | `double precision` | YES |  |  |
| `commodity` | `character varying(255)` | YES |  |  |
| `carrier` | `character varying(255)` | YES |  |  |
| `ref` | `character varying(255)` | YES |  |  |
| `pre_carrier_vsl` | `character varying(255)` | YES |  |  |
| `master_vessel` | `character varying(255)` | YES |  |  |
| `loading_port` | `character varying(255)` | YES |  |  |
| `loading_country` | `character varying(255)` | YES |  |  |
| `eta` | `timestamp with time zone` | YES |  |  |
| `etd` | `timestamp with time zone` | YES |  |  |
| `discharge_port` | `character varying(255)` | YES |  |  |
| `discharge_country` | `character varying(255)` | YES |  |  |
| `final_destination` | `character varying(255)` | YES |  |  |
| `eta_pod` | `timestamp with time zone` | YES |  |  |
| `eta_destn` | `timestamp with time zone` | YES |  |  |
| `pick_up_ref` | `character varying(255)` | YES |  |  |
| `warehouse` | `character varying(255)` | YES |  |  |
| `buyer_id` | `bigint(64,0)` | YES |  | FK → `public.buyer.id` |
| `vendor_id` | `bigint(64,0)` | YES |  | FK → `public.vendor.id` |
| `booking_request_id` | `bigint(64,0)` | YES |  | FK → `public.booking_request.id` |
| `loading_address` | `character varying(255)` | YES |  |  |
| `container_quantity` | `double precision` | YES |  |  |
| `warehouse_country` | `character varying(255)` | YES |  |  |
| `loading_address_detail` | `character varying(500)` | YES |  |  |
| `final_destination_detail` | `character varying(500)` | YES |  |  |
| `carrier_branch` | `character varying(255)` | YES |  |  |
| `regional_office` | `character varying(255)` | YES |  |  |
| `office_address` | `character varying(500)` | YES |  |  |
| `place_of_receipt` | `character varying(255)` | YES |  |  |
| `destination_country` | `character varying(255)` | YES |  |  |
| `destination_port` | `character varying(255)` | YES |  |  |
| `warehouse_uuid` | `character varying(36)` | YES |  |  |

#### `public.booking_request`

- **Type:** BASE TABLE  **Rows:** 233

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('booking_request_id_seq'::reg... | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `is_project` | `boolean` | NO |  |  |
| `project_uuid` | `character varying(255)` | YES |  |  |
| `project_code` | `character varying(255)` | YES |  |  |
| `project_title` | `character varying(255)` | YES |  |  |
| `title` | `character varying(255)` | YES |  |  |
| `approval_route_uuid` | `character varying(255)` | YES |  |  |
| `approval_route_name` | `character varying(255)` | YES |  |  |
| `approval_route_sequence` | `text` | YES |  |  |
| `next_approver_group_uuid` | `character varying(255)` | YES |  |  |
| `next_approver` | `character varying(255)` | YES |  |  |
| `approved_date` | `timestamp with time zone` | YES |  |  |
| `requester_uuid` | `character varying(255)` | NO |  |  |
| `requester_name` | `character varying(255)` | NO |  |  |
| `submitted_date` | `timestamp with time zone` | NO |  |  |
| `updated_date` | `timestamp with time zone` | NO |  |  |
| `booking_request_no` | `character varying(255)` | YES |  |  |
| `currency_code` | `character varying(255)` | NO |  |  |
| `currency_name` | `character varying(255)` | NO |  |  |
| `status` | `character varying(255)` | NO |  |  |
| `buyer_id` | `bigint(64,0)` | NO |  | FK → `public.buyer.id` |
| `vendor_id` | `bigint(64,0)` | NO |  | FK → `public.vendor.id` |
| `payment_term_uuid` | `character varying(255)` | YES |  |  |
| `payment_term_name` | `character varying(255)` | YES |  |  |
| `container_type` | `character varying(255)` | NO |  |  |
| `is_break_bulk_shipping` | `boolean` | YES |  |  |
| `dimension_length` | `double precision` | YES |  |  |
| `dimension_length_uom` | `character varying(255)` | YES |  |  |
| `dimension_breadth` | `double precision` | YES |  |  |
| `dimension_breadth_uom` | `character varying(255)` | YES |  |  |
| `dimension_height` | `double precision` | YES |  |  |
| `dimension_height_uom` | `character varying(255)` | YES |  |  |
| `volumetric` | `double precision` | YES |  |  |
| `volumetric_uom` | `character varying(255)` | YES |  |  |
| `weight` | `double precision` | YES |  |  |
| `weight_uom` | `character varying(255)` | NO |  |  |
| `hs_code` | `character varying(255)` | YES |  |  |
| `commodity` | `character varying(255)` | YES |  |  |
| `is_hazardous_goods` | `boolean` | NO |  |  |
| `msds_code` | `character varying(255)` | YES |  |  |
| `door_service_type` | `character varying(255)` | NO |  |  |
| `cargo_will_be_ready_date` | `timestamp with time zone` | YES |  |  |
| `loading_country` | `character varying(255)` | NO |  |  |
| `loading_port` | `character varying(255)` | NO |  |  |
| `loading_address` | `character varying(255)` | YES |  |  |
| `discharge_country` | `character varying(255)` | NO |  |  |
| `discharge_port` | `character varying(255)` | NO |  |  |
| `final_destination` | `character varying(255)` | YES |  |  |
| `is_custom_clearance` | `boolean` | NO |  |  |
| `total_amount` | `double precision` | NO |  |  |
| `is_confirmed_by_buyer_and_supplier` | `boolean` | NO |  |  |
| `invoiced_amount` | `double precision` | YES | 0 |  |
| `has_proposed_price` | `boolean` | YES | false |  |
| `loading_address_detail` | `character varying(500)` | YES |  |  |
| `final_destination_detail` | `character varying(500)` | YES |  |  |
| `same_as_buyer` | `boolean` | YES | false |  |
| `shipper_name` | `character varying(255)` | YES |  |  |
| `shipper_email` | `character varying(255)` | YES |  |  |
| `shipper_dual_code` | `character varying(255)` | YES |  |  |
| `shipper_phone` | `character varying(255)` | YES |  |  |
| `shipper_address` | `character varying(255)` | YES |  |  |
| `shipper_uen` | `character varying(255)` | YES |  |  |
| `shipper_address_detail` | `character varying(500)` | YES |  |  |
| `destination_country` | `character varying(255)` | YES |  |  |
| `destination_port` | `character varying(255)` | YES |  |  |
| `valid_from` | `timestamp with time zone` | YES |  |  |
| `valid_to` | `timestamp with time zone` | YES |  |  |
| `rfq_id` | `bigint(64,0)` | YES |  |  |
| `is_from_true_supplier` | `boolean` | YES |  |  |
| `is_reference_po` | `boolean` | YES | false |  |
| `po_role` | `character varying(20)` | YES |  |  |
| `term_and_condition` | `text` | YES |  |  |
| `loading_address_uuid` | `character varying(36)` | YES |  |  |
| `final_destination_uuid` | `character varying(36)` | YES |  |  |
| `shipper_address_uuid` | `character varying(36)` | YES |  |  |
| `payment_terms_days` | `integer(32,0)` | YES |  |  |

#### `public.booking_request_audit_trail`

- **Type:** BASE TABLE  **Rows:** 699

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('booking_request_audit_trail_... | PK |
| `user_name` | `character varying(255)` | NO |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | NO |  |  |
| `action` | `character varying(255)` | NO |  |  |
| `date_time` | `timestamp with time zone` | NO |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `booking_request_id` | `bigint(64,0)` | NO |  | FK → `public.booking_request.id` |
| `note` | `character varying(50)` | YES |  |  |

**Indexes:**
- `booking_request_audit_trail_pk`: `CREATE UNIQUE INDEX booking_request_audit_trail_pk ON public.booking_request_audit_trail USING btree (id)`

#### `public.booking_request_document`

- **Type:** BASE TABLE  **Rows:** 23

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('booking_request_document_id_... | PK |
| `guid` | `character varying(255)` | NO |  |  |
| `label` | `character varying(255)` | YES |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `description` | `character varying(255)` | YES |  |  |
| `uploaded_by` | `character varying(255)` | NO |  |  |
| `uploader_uuid` | `character varying(255)` | NO |  |  |
| `uploaded_on` | `timestamp with time zone` | NO |  |  |
| `external` | `boolean` | NO |  |  |
| `booking_request_id` | `bigint(64,0)` | NO |  | FK → `public.booking_request.id` |

#### `public.booking_request_goods_movement`

- **Type:** BASE TABLE  **Rows:** 66

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('booking_request_goods_moveme... |  |
| `uuid` | `character varying(255)` | NO |  |  |
| `booking_request_uuid` | `character varying(255)` | NO |  |  |
| `action` | `character varying(255)` | NO |  |  |
| `remarks` | `character varying(255)` | YES |  |  |
| `updated_at` | `timestamp with time zone` | NO |  |  |
| `updated_by` | `character varying(255)` | NO |  |  |
| `updated_by_name` | `character varying(255)` | NO |  |  |

#### `public.booking_request_msds`

- **Type:** BASE TABLE  **Rows:** 58

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('booking_request_msds_id_seq'... | PK |
| `guid` | `character varying(255)` | NO |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `booking_request_id` | `bigint(64,0)` | NO |  | FK → `public.booking_request.id` |

#### `public.booking_request_ocean_freight`

- **Type:** BASE TABLE  **Rows:** 365

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('booking_request_ocean_freigh... | PK |
| `item_name` | `character varying(255)` | NO |  |  |
| `is_reefer` | `boolean` | NO |  |  |
| `uom` | `character varying(255)` | YES |  |  |
| `quantity` | `numeric(25,12)` | NO |  |  |
| `currency_code` | `character varying(255)` | NO |  |  |
| `unit_price` | `numeric(25,12)` | NO |  |  |
| `exchange_rate` | `double precision` | NO |  |  |
| `remark` | `character varying(500)` | YES |  |  |
| `booking_request_id` | `bigint(64,0)` | NO |  | FK → `public.booking_request.id` |
| `tax_code` | `character varying(255)` | YES |  |  |
| `tax_percentage` | `double precision` | YES |  |  |
| `invoiced_amount` | `numeric(25,12)` | YES | 0 |  |
| `invoiced_quantity` | `numeric(25,12)` | YES | 0 |  |
| `uuid` | `character varying(255)` | YES |  |  |
| `proposed_price` | `numeric(25,12)` | YES |  |  |
| `item_code` | `character varying(255)` | YES |  |  |
| `is_manual` | `boolean` | YES | false |  |
| `come_from_fcl` | `boolean` | YES | false |  |
| `sc_no` | `character varying(50)` | YES |  |  |
| `valid_from` | `timestamp with time zone` | YES |  |  |
| `valid_to` | `timestamp with time zone` | YES |  |  |
| `internal_remark` | `character varying(500)` | YES |  |  |
| `external_remark` | `character varying(500)` | YES |  |  |
| `carrier` | `character varying(100)` | YES |  |  |
| `tax_uuid` | `character varying` | YES |  |  |

#### `public.booking_request_purchase_orders`

- **Type:** BASE TABLE  **Rows:** 8

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('booking_request_purchase_ord... |  |
| `booking_request_id` | `bigint(64,0)` | NO |  | FK → `public.booking_request.id` |
| `purchase_order_id` | `bigint(64,0)` | YES |  |  |
| `purchase_order_no` | `character varying(255)` | NO |  |  |
| `purchase_order_uuid` | `character varying(255)` | NO |  |  |

#### `public.booking_request_shipping_container`

- **Type:** BASE TABLE  **Rows:** 87

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('booking_request_shipping_con... | PK |
| `item_name` | `character varying(255)` | NO |  |  |
| `quantity` | `double precision` | NO |  |  |
| `is_reefer` | `boolean` | NO |  |  |
| `booking_request_id` | `bigint(64,0)` | NO |  | FK → `public.booking_request.id` |

#### `public.booking_request_subject_to`

- **Type:** BASE TABLE  **Rows:** 144

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('booking_request_subject_to_i... | PK |
| `item_name` | `character varying(255)` | NO |  |  |
| `uom` | `character varying(255)` | NO |  |  |
| `quantity` | `numeric(25,12)` | NO |  |  |
| `currency_code` | `character varying(255)` | NO |  |  |
| `unit_price` | `numeric(25,12)` | NO |  |  |
| `exchange_rate` | `double precision` | NO |  |  |
| `remark` | `character varying(255)` | YES |  |  |
| `booking_request_id` | `bigint(64,0)` | NO |  | FK → `public.booking_request.id` |
| `tax_code` | `character varying(255)` | YES |  |  |
| `tax_percentage` | `double precision` | YES |  |  |
| `invoiced_amount` | `numeric(25,12)` | YES | 0 |  |
| `invoiced_quantity` | `numeric(25,12)` | YES | 0 |  |
| `uuid` | `character varying(255)` | YES |  |  |
| `proposed_price` | `numeric(25,12)` | YES |  |  |
| `item_code` | `character varying(255)` | YES |  |  |
| `is_manual` | `boolean` | YES | false |  |
| `tax_uuid` | `character varying` | YES |  |  |

#### `public.buyer`

- **Type:** BASE TABLE  **Rows:** 2731

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('buyer_id_seq'::regclass) | PK |
| `company_name` | `character varying(255)` | NO |  |  |
| `uen` | `character varying(255)` | NO |  |  |
| `country_of_origin` | `character varying(255)` | NO |  |  |
| `gst_reg_no` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `address_label` | `character varying(500)` | NO |  |  |
| `address_first_line` | `character varying(500)` | NO |  |  |
| `address_second_line` | `character varying(255)` | YES |  |  |
| `city` | `character varying(255)` | YES |  |  |
| `state` | `character varying(255)` | NO |  |  |
| `country` | `character varying(255)` | NO |  |  |
| `postal_code` | `character varying(255)` | NO |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `email` | `character varying(255)` | NO |  |  |
| `country_code` | `character varying(255)` | NO |  |  |
| `phone_number` | `character varying(255)` | NO |  |  |
| `uuid` | `character varying(255)` | YES |  |  |
| `company_code` | `character varying(255)` | YES |  |  |
| `address_uuid` | `character varying(255)` | YES |  |  |
| `md5_checksum` | `character varying(255)` | YES |  |  |

#### `public.bwh_debit_note`

- **Type:** BASE TABLE  **Rows:** 319

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('bwh_debit_note_id_seq'::regc... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `number` | `character varying(255)` | YES |  |  |
| `global_number` | `character varying(255)` | YES |  |  |
| `status` | `character varying(50)` | YES |  |  |
| `debit_note_date` | `timestamp without time zone` | YES |  |  |
| `submission_date` | `timestamp without time zone` | YES |  |  |
| `tax_amount` | `numeric(19,4)` | YES | 0 |  |
| `aggregate_tax_amount` | `numeric(19,4)` | YES |  |  |
| `sub_total` | `numeric(19,4)` | YES | 0 |  |
| `total_amount` | `numeric(19,4)` | YES | 0 |  |
| `total_amount_document_currency` | `numeric(19,4)` | YES | 0 |  |
| `currency_code` | `character varying(50)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `remarks` | `text` | YES |  |  |
| `buyer_id` | `bigint(64,0)` | YES |  | FK → `public.buyer.id` |
| `vendor_id` | `bigint(64,0)` | YES |  | FK → `public.vendor.id` |
| `requester_name` | `character varying(255)` | YES |  |  |
| `requester_uuid` | `character varying(255)` | YES |  |  |
| `dn_approval_date` | `timestamp without time zone` | YES |  |  |
| `payment_status` | `character varying(50)` | YES |  |  |
| `payment_number` | `character varying(255)` | YES |  |  |
| `paid_amount` | `numeric(19,4)` | YES | 0 |  |
| `processing_payment_amt` | `numeric(19,4)` | YES | 0 |  |
| `paid_payment_amount` | `numeric(19,4)` | YES | 0 |  |
| `processing_amt` | `numeric(19,4)` | YES | 0 |  |
| `updated_date` | `timestamp without time zone` | YES |  |  |
| `invoice_uuid` | `character varying(255)` | YES |  |  |
| `invoice_number` | `character varying(255)` | YES |  |  |
| `invoice_status` | `character varying(255)` | YES |  |  |
| `project_uuid` | `character varying(255)` | YES |  |  |
| `project_code` | `character varying(255)` | YES |  |  |
| `project_title` | `character varying(255)` | YES |  |  |
| `note` | `text` | YES |  |  |

#### `public.bwh_debit_note_document_metadata`

- **Type:** BASE TABLE  **Rows:** 0

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('bwh_debit_note_document_meta... | PK |
| `guid` | `character varying(255)` | YES |  |  |
| `file_label` | `character varying(255)` | YES |  |  |
| `file_name` | `character varying(255)` | YES |  |  |
| `file_description` | `text` | YES |  |  |
| `uploaded_on` | `timestamp without time zone` | YES |  |  |
| `uploaded_by_name` | `character varying(255)` | YES |  |  |
| `uploaded_by_uuid` | `character varying(255)` | YES |  |  |
| `external_document` | `boolean` | YES |  |  |
| `debit_note_id` | `bigint(64,0)` | YES |  | FK → `public.bwh_debit_note.id` |

#### `public.bwh_debit_note_item`

- **Type:** BASE TABLE  **Rows:** 494

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('bwh_debit_note_item_id_seq':... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `code` | `character varying(255)` | YES |  |  |
| `description` | `character varying(1000)` | YES |  |  |
| `quantity` | `numeric(19,4)` | YES | 0 |  |
| `currency` | `character varying(50)` | YES |  |  |
| `unit_price` | `numeric(19,4)` | YES | 0 |  |
| `tax_code` | `character varying(255)` | YES |  |  |
| `net_price` | `numeric(19,4)` | YES | 0 |  |
| `uom_code` | `character varying(100)` | YES |  |  |
| `tax_uuid` | `character varying(255)` | YES |  |  |
| `tax_percent` | `numeric(10,2)` | YES | 0 |  |
| `notes` | `text` | YES |  |  |
| `image_url` | `text` | YES |  |  |
| `cat_item_uuid` | `character varying(255)` | YES |  |  |
| `bwh_debit_note_id` | `bigint(64,0)` | YES |  | FK → `public.bwh_debit_note.id` |
| `name` | `character varying(255)` | YES |  |  |

#### `public.bwh_debitnote_audit_trail`

- **Type:** BASE TABLE  **Rows:** 935

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('bwh_debitnote_audit_trail_id... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `action` | `character varying(255)` | YES |  |  |
| `date_time` | `timestamp without time zone` | YES |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `bwh_debit_note_id` | `bigint(64,0)` | YES |  | FK → `public.bwh_debit_note.id` |
| `dn_status` | `character varying(50)` | YES |  |  |

#### `public.carrier`

- **Type:** BASE TABLE  **Rows:** 262

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('carrier_id_seq'::regclass) | PK |
| `carrier_name` | `character varying(100)` | YES |  |  |
| `abbreviation` | `character varying(50)` | YES |  |  |
| `carrier_branch` | `character varying(255)` | YES |  |  |
| `regional_office` | `character varying(255)` | YES |  |  |
| `office_address` | `character varying(500)` | YES |  |  |

#### `public.contact_person`

- **Type:** BASE TABLE  **Rows:** 4605

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('contact_person_id_seq'::regc... | PK |
| `uuid` | `character varying(36)` | NO |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `email` | `character varying(255)` | YES |  |  |
| `phone_number` | `character varying(50)` | YES |  |  |
| `country_code` | `character varying(10)` | YES |  |  |

#### `public.dn_inbound_outbound_mapping`

- **Type:** BASE TABLE  **Rows:** 399

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('dn_inbound_outbound_mapping_... | PK |
| `type` | `character varying(50)` | YES |  |  |
| `debit_note_id` | `bigint(64,0)` | NO |  | FK → `public.bwh_debit_note.id` |
| `inbound_request_id` | `bigint(64,0)` | YES |  | FK → `public.inbound_request.id` |
| `outbound_request_id` | `bigint(64,0)` | YES |  | FK → `public.outbound_request.id` |

#### `public.email_template`

- **Type:** BASE TABLE  **Rows:** 54

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('email_template_id_seq'::regc... | PK |
| `feature_code` | `character varying(50)` | YES |  |  |
| `action` | `character varying(50)` | YES |  |  |
| `subject` | `character varying(500)` | YES |  |  |
| `content` | `text` | YES |  |  |

**Indexes:**
- `email_template_id_uindex`: `CREATE UNIQUE INDEX email_template_id_uindex ON public.email_template USING btree (id)`
- `email_template_pk`: `CREATE UNIQUE INDEX email_template_pk ON public.email_template USING btree (id)`

#### `public.goods_details`

- **Type:** BASE TABLE  **Rows:** 5045

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('goods_details_id_seq'::regcl... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `driver_id_no` | `character varying(255)` | YES |  |  |
| `packages` | `integer(32,0)` | YES |  |  |
| `estimated_arrival_date` | `timestamp without time zone` | YES |  |  |
| `truck_no` | `character varying(255)` | YES |  |  |
| `seal_no` | `character varying(255)` | YES |  |  |
| `note` | `text` | YES |  |  |
| `pick_up_time` | `timestamp without time zone` | YES |  |  |
| `goods_receiving_id` | `bigint(64,0)` | YES |  | FK → `public.goods_receiving.id` |
| `contact_person_id` | `bigint(64,0)` | YES |  | FK → `public.contact_person.id` |
| `container_no` | `character varying(255)` | YES |  |  |

#### `public.goods_receiving`

- **Type:** BASE TABLE  **Rows:** 4918

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('goods_receiving_id_seq'::reg... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `is_bwh_delivery_goods` | `boolean` | YES |  |  |
| `address_id` | `bigint(64,0)` | YES |  | FK → `public.address.id` |

#### `public.house_bl`

- **Type:** BASE TABLE  **Rows:** 106

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('house_bl_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `bl_no` | `character varying(255)` | YES |  |  |
| `number_of_original_bl` | `integer(32,0)` | YES |  |  |
| `buyer_id` | `bigint(64,0)` | NO |  | FK → `public.buyer.id` |
| `vendor_id` | `bigint(64,0)` | NO |  | FK → `public.vendor.id` |
| `house_bl_title` | `character varying(255)` | YES |  |  |
| `requester_uuid` | `character varying(255)` | YES |  |  |
| `requester_name` | `character varying(255)` | YES |  |  |
| `converted_date` | `timestamp with time zone` | NO |  |  |
| `submitted_date` | `timestamp with time zone` | YES |  |  |
| `updated_date` | `timestamp with time zone` | NO |  |  |
| `status` | `character varying(255)` | NO |  |  |
| `freight_and_disbursements` | `character varying(255)` | YES |  |  |
| `rate_at` | `character varying(255)` | YES |  |  |
| `prepaid` | `character varying(255)` | YES |  |  |
| `collect` | `character varying(255)` | YES |  |  |
| `shipping_instruction_id` | `bigint(64,0)` | NO |  | FK → `public.shipping_instruction.id` |
| `can_invoice` | `boolean` | YES | true |  |
| `master_bl_label` | `character varying(255)` | YES |  |  |
| `ams_scac_code` | `character varying(255)` | YES |  |  |
| `is_use_system_generated_bl` | `boolean` | YES | true |  |

#### `public.house_bl_audit_trail`

- **Type:** BASE TABLE  **Rows:** 323

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('house_bl_audit_trail_id_seq'... | PK |
| `user_name` | `character varying(255)` | NO |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | NO |  |  |
| `action` | `character varying(255)` | NO |  |  |
| `date_time` | `timestamp with time zone` | NO |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `house_bl_id` | `bigint(64,0)` | NO |  | FK → `public.house_bl.id` |
| `pdf_version` | `character varying(255)` | YES |  |  |
| `is_use_system_generated_bl` | `boolean` | YES | true |  |
| `list_template_files` | `character varying(2000)` | YES |  |  |

**Indexes:**
- `house_bl_audit_trail_pk`: `CREATE UNIQUE INDEX house_bl_audit_trail_pk ON public.house_bl_audit_trail USING btree (id)`

#### `public.house_bl_document`

- **Type:** BASE TABLE  **Rows:** 5

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('house_bl_document_id_seq'::r... | PK |
| `guid` | `character varying(255)` | NO |  |  |
| `label` | `character varying(255)` | YES |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `description` | `character varying(255)` | YES |  |  |
| `uploaded_by` | `character varying(255)` | NO |  |  |
| `uploader_uuid` | `character varying(255)` | NO |  |  |
| `uploaded_on` | `timestamp with time zone` | NO |  |  |
| `external` | `boolean` | NO |  |  |
| `house_bl_id` | `bigint(64,0)` | NO |  | FK → `public.house_bl.id` |

#### `public.house_bl_master_bl`

- **Type:** BASE TABLE  **Rows:** 63

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('house_bl_master_bl_id_seq'::... | PK |
| `guid` | `character varying(255)` | NO |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `uploaded_on` | `timestamp with time zone` | NO |  |  |
| `house_bl_id` | `bigint(64,0)` | NO |  | FK → `public.house_bl.id` |

#### `public.house_bl_template_files`

- **Type:** BASE TABLE  **Rows:** 7

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('house_bl_template_files_id_s... | PK |
| `guid` | `character varying(255)` | NO |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `uploaded_on` | `timestamp with time zone` | NO |  |  |
| `house_bl_id` | `bigint(64,0)` | NO |  | FK → `public.house_bl.id` |

#### `public.hs_code`

- **Type:** BASE TABLE  **Rows:** 11419

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('hs_code_id_seq'::regclass) | PK |
| `hs_code` | `character varying(255)` | YES |  |  |
| `hs_description` | `character varying(255)` | YES |  |  |
| `hs_uom` | `character varying(50)` | YES |  |  |
| `reference_id` | `character varying(255)` | YES |  |  |

#### `public.inbound_processing_status`

- **Type:** BASE TABLE  **Rows:** 12

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('inbound_processing_status_id... | PK |
| `uuid` | `character varying(36)` | NO |  |  |
| `action` | `character varying(255)` | YES |  |  |
| `remarks` | `text` | YES |  |  |
| `updated_by` | `character varying(255)` | YES |  |  |
| `updated_on` | `timestamp without time zone` | YES |  |  |
| `inbound_request_id` | `bigint(64,0)` | NO |  | FK → `public.inbound_request.id` |

**Indexes:**
- `inbound_processing_status_uuid_key`: `CREATE UNIQUE INDEX inbound_processing_status_uuid_key ON public.inbound_processing_status USING btree (uuid)`

#### `public.inbound_req_audit_trail`

- **Type:** BASE TABLE  **Rows:** 3544

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('inbound_req_audit_trail_id_s... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `action` | `character varying(255)` | YES |  |  |
| `date_time` | `timestamp without time zone` | YES |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `ir_status` | `character varying(255)` | YES |  |  |
| `inbound_request_id` | `bigint(64,0)` | NO |  | FK → `public.inbound_request.id` |

#### `public.inbound_request`

- **Type:** BASE TABLE  **Rows:** 1942

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('inbound_request_id_seq'::reg... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `ir_number` | `character varying(50)` | YES |  |  |
| `invoice_no` | `character varying(50)` | YES |  |  |
| `bl_no` | `character varying(50)` | YES |  |  |
| `driver_id_no` | `character varying(255)` | YES |  |  |
| `is_project` | `boolean` | YES |  |  |
| `is_bwh_custom_declaration` | `boolean` | YES |  |  |
| `currency_code` | `character varying(50)` | YES |  |  |
| `currency_name` | `character varying(255)` | YES |  |  |
| `total_amount` | `numeric(26,2)` | YES | 0 |  |
| `estimated_gross_weight` | `bigint(64,0)` | YES | 0 |  |
| `estimated_volume` | `bigint(64,0)` | YES | 0 |  |
| `actual_gross_weight` | `bigint(64,0)` | YES | 0 |  |
| `actual_volume` | `bigint(64,0)` | YES | 0 |  |
| `estimated_no_packages` | `bigint(64,0)` | YES | 0 |  |
| `actual_no_of_packages` | `bigint(64,0)` | YES | 0 |  |
| `project_code` | `character varying(50)` | YES |  |  |
| `project_title` | `character varying(100)` | YES |  |  |
| `project_uuid` | `character varying(255)` | YES |  |  |
| `ir_title` | `character varying(255)` | YES |  |  |
| `submitted_date` | `timestamp with time zone` | NO | now() |  |
| `updated_date` | `timestamp with time zone` | NO | now() |  |
| `note` | `text` | YES |  |  |
| `ir_status` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `requisition_type` | `character varying(100)` | YES |  |  |
| `requisition_nature` | `character varying(100)` | YES |  |  |
| `vendor_id` | `bigint(64,0)` | YES |  | FK → `public.vendor.id` |
| `actual_inbound_date` | `timestamp with time zone` | YES |  |  |
| `goods_receiving_id` | `bigint(64,0)` | YES |  | FK → `public.goods_receiving.id` |
| `remarks` | `text` | YES |  |  |
| `buyer_id` | `bigint(64,0)` | YES |  | FK → `public.buyer.id` |

#### `public.inbound_request_document_metadata`

- **Type:** BASE TABLE  **Rows:** 1353

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('inbound_request_document_met... | PK |
| `guid` | `character varying(50)` | YES |  |  |
| `file_label` | `character varying(255)` | YES |  |  |
| `file_description` | `character varying(255)` | YES |  |  |
| `uploaded_on` | `timestamp with time zone` | NO | now() |  |
| `uploaded_by` | `character varying(100)` | YES |  |  |
| `uploader_uuid` | `character varying(50)` | YES |  |  |
| `external_document` | `boolean` | YES |  |  |
| `declaration_no` | `character varying(100)` | YES |  |  |
| `ir_id` | `bigint(64,0)` | YES |  | FK → `public.inbound_request.id` |
| `file_name` | `character varying(255)` | YES |  |  |

#### `public.inbound_request_goods_movement`

- **Type:** BASE TABLE  **Rows:** 91

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('inbound_request_goods_moveme... |  |
| `uuid` | `character varying(36)` | NO |  |  |
| `action` | `character varying(255)` | YES |  |  |
| `remarks` | `character varying(255)` | YES |  |  |
| `updated_by` | `character varying(255)` | YES |  |  |
| `updated_at` | `timestamp with time zone` | NO |  |  |
| `updated_by_name` | `character varying(255)` | NO |  |  |
| `inbound_request_id` | `bigint(64,0)` | NO |  | FK → `public.inbound_request.id` |

**Indexes:**
- `inbound_request_goods_movement_uuid_key`: `CREATE UNIQUE INDEX inbound_request_goods_movement_uuid_key ON public.inbound_request_goods_movement USING btree (uuid)`

#### `public.inbound_request_item`

- **Type:** BASE TABLE  **Rows:** 2732

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('inbound_request_item_id_seq'... | PK |
| `code` | `character varying(100)` | YES |  |  |
| `name` | `character varying(255)` | YES |  |  |
| `description` | `text` | YES |  |  |
| `source_currency` | `character varying(50)` | YES |  |  |
| `unit_price` | `numeric(25,2)` | YES |  |  |
| `request_quantity` | `numeric(25,2)` | YES |  |  |
| `actual_inbound_quantity` | `numeric(25,2)` | YES |  |  |
| `outbound_quantity` | `numeric(25,2)` | YES |  |  |
| `remaining_quantity` | `numeric(25,2)` | YES |  |  |
| `price_type` | `character varying(100)` | YES |  |  |
| `tax_code` | `character varying(50)` | YES |  |  |
| `tax_rate` | `numeric(25,2)` | YES | 0 |  |
| `tax_uuid` | `character varying(255)` | YES |  |  |
| `note` | `character varying(3000)` | YES |  |  |
| `ir_id` | `bigint(64,0)` | YES |  | FK → `public.inbound_request.id` |
| `cat_item_id` | `bigint(64,0)` | YES |  |  |
| `manual_item` | `boolean` | YES |  |  |
| `sub_total` | `numeric(26,2)` | YES | 0 |  |
| `tax_amount` | `numeric(26,2)` | YES | 0 |  |
| `total_amount` | `numeric(26,2)` | YES | 0 |  |
| `company_uuid` | `character varying(50)` | YES |  |  |
| `uom` | `character varying(50)` | YES |  |  |
| `uuid` | `character varying(255)` | NO |  |  |
| `outbound_processing` | `numeric(25,2)` | YES |  |  |
| `hs_code` | `character varying(255)` | YES |  |  |
| `outer_uom` | `character varying(50)` | YES |  |  |
| `requested_outer_quantity` | `numeric(25,2)` | YES | 0 |  |
| `actual_outer_quantity` | `numeric(25,2)` | YES | 0 |  |
| `actual_outbound_outer_quantity` | `numeric(25,2)` | YES | 0 |  |
| `remaining_outer_quantity` | `numeric(25,2)` | YES | 0 |  |
| `outer_outbound_processing` | `numeric(25,2)` | YES | 0 |  |

**Indexes:**
- `uk_inbound_request_item_uuid`: `CREATE UNIQUE INDEX uk_inbound_request_item_uuid ON public.inbound_request_item USING btree (uuid)`

#### `public.liquibase-changelog`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `character varying(255)` | NO |  |  |
| `author` | `character varying(255)` | NO |  |  |
| `filename` | `character varying(255)` | NO |  |  |
| `dateexecuted` | `timestamp without time zone` | NO |  |  |
| `orderexecuted` | `integer(32,0)` | NO |  |  |
| `exectype` | `character varying(10)` | NO |  |  |
| `md5sum` | `character varying(35)` | YES |  |  |
| `description` | `character varying(255)` | YES |  |  |
| `comments` | `character varying(255)` | YES |  |  |
| `tag` | `character varying(255)` | YES |  |  |
| `liquibase` | `character varying(20)` | YES |  |  |
| `contexts` | `character varying(255)` | YES |  |  |
| `labels` | `character varying(255)` | YES |  |  |
| `deployment_id` | `character varying(10)` | YES |  |  |

#### `public.liquibase-lock`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO |  | PK |
| `locked` | `boolean` | NO |  |  |
| `lockgranted` | `timestamp without time zone` | YES |  |  |
| `lockedby` | `character varying(255)` | YES |  |  |

#### `public.outbound_req_audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('outbound_req_audit_trail_id_... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `action` | `character varying(255)` | YES |  |  |
| `date_time` | `timestamp without time zone` | YES |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `or_status` | `character varying(255)` | YES |  |  |
| `outbound_request_id` | `bigint(64,0)` | YES |  | FK → `public.outbound_request.id` |

#### `public.outbound_request`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('outbound_request_id_seq'::re... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `or_number` | `character varying(50)` | YES |  |  |
| `requisition_type` | `character varying(100)` | YES |  |  |
| `or_status` | `character varying(255)` | YES |  |  |
| `currency_code` | `character varying(255)` | YES |  |  |
| `currency_name` | `character varying(255)` | YES |  |  |
| `or_title` | `character varying(255)` | YES |  |  |
| `delivery_no` | `character varying(255)` | YES |  |  |
| `estimated_gross_weight` | `bigint(64,0)` | YES | 0 |  |
| `estimated_volume` | `bigint(64,0)` | YES | 0 |  |
| `actual_gross_weight` | `bigint(64,0)` | YES | 0 |  |
| `actual_volume` | `bigint(64,0)` | YES | 0 |  |
| `estimated_no_packages` | `bigint(64,0)` | YES | 0 |  |
| `actual_no_of_packages` | `bigint(64,0)` | YES | 0 |  |
| `is_bwh_custom_declaration` | `boolean` | YES |  |  |
| `note` | `text` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `driver_id_no` | `character varying(255)` | YES |  |  |
| `remarks` | `text` | YES |  |  |
| `submitted_date` | `timestamp with time zone` | NO | now() |  |
| `updated_date` | `timestamp with time zone` | NO | now() |  |
| `vendor_id` | `bigint(64,0)` | YES |  | FK → `public.vendor.id` |
| `goods_receiving_id` | `bigint(64,0)` | YES |  | FK → `public.goods_receiving.id` |
| `new_owner_id` | `bigint(64,0)` | YES |  | FK → `public.vendor.id` |
| `buyer_id` | `bigint(64,0)` | YES |  | FK → `public.buyer.id` |
| `actual_outbound_date` | `timestamp with time zone` | YES |  |  |
| `total_amount` | `numeric(26,2)` | YES | 0 |  |
| `sub_total` | `numeric(26,2)` | YES | 0 |  |

#### `public.outbound_request_document_metadata`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('outbound_request_document_me... | PK |
| `guid` | `character varying(50)` | YES |  |  |
| `file_label` | `character varying(255)` | YES |  |  |
| `file_description` | `character varying(255)` | YES |  |  |
| `uploaded_on` | `timestamp with time zone` | NO | now() |  |
| `uploaded_by` | `character varying(100)` | YES |  |  |
| `uploader_uuid` | `character varying(50)` | YES |  |  |
| `external_document` | `boolean` | YES |  |  |
| `file_name` | `character varying(255)` | YES |  |  |
| `declaration_no` | `character varying(100)` | YES |  |  |
| `or_id` | `bigint(64,0)` | YES |  | FK → `public.outbound_request.id` |

#### `public.outbound_request_goods_movement`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('outbound_request_goods_movem... |  |
| `uuid` | `character varying(36)` | NO |  |  |
| `action` | `character varying(255)` | YES |  |  |
| `remarks` | `character varying(255)` | YES |  |  |
| `updated_by` | `character varying(255)` | YES |  |  |
| `updated_at` | `timestamp with time zone` | NO |  |  |
| `updated_by_name` | `character varying(255)` | NO |  |  |
| `outbound_request_id` | `bigint(64,0)` | NO |  | FK → `public.outbound_request.id` |

**Indexes:**
- `outbound_request_goods_movement_uuid_key`: `CREATE UNIQUE INDEX outbound_request_goods_movement_uuid_key ON public.outbound_request_goods_movement USING btree (uuid)`

#### `public.outbound_request_item`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('outbound_request_item_id_seq... | PK |
| `request_qty` | `numeric(25,2)` | YES | 0 |  |
| `actual_qty` | `numeric(25,2)` | YES | 0 |  |
| `inbound_request_item_id` | `bigint(64,0)` | YES |  | FK → `public.inbound_request_item.id` |
| `outbound_request_id` | `bigint(64,0)` | YES |  | FK → `public.outbound_request.id` |
| `total_amount` | `numeric(19,2)` | YES | 0 |  |
| `uuid` | `character varying(255)` | NO |  |  |
| `note` | `text` | YES |  |  |
| `hs_code` | `character varying(255)` | YES |  |  |
| `requested_outer_quantity` | `numeric(25,2)` | YES | 0 |  |
| `actual_outer_quantity` | `numeric(25,2)` | YES | 0 |  |

**Indexes:**
- `uk_outbound_request_item_uuid`: `CREATE UNIQUE INDEX uk_outbound_request_item_uuid ON public.outbound_request_item USING btree (uuid)`

#### `public.outbound_request_mapping`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('outbound_request_mapping_id_... | PK |
| `outbound_request_id` | `bigint(64,0)` | YES |  | FK → `public.outbound_request.id` |
| `inbound_request_id` | `bigint(64,0)` | YES |  | FK → `public.inbound_request.id` |

#### `public.request_for_quotation`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('request_for_quotation_id_seq... | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `is_project` | `boolean` | NO |  |  |
| `project_uuid` | `character varying(255)` | YES |  |  |
| `project_code` | `character varying(255)` | YES |  |  |
| `project_title` | `character varying(255)` | YES |  |  |
| `title` | `character varying(255)` | NO |  |  |
| `approval_route_uuid` | `character varying(255)` | YES |  |  |
| `approval_route_name` | `character varying(255)` | YES |  |  |
| `approval_route_sequence` | `text` | YES |  |  |
| `next_approver_group_uuid` | `character varying(255)` | YES |  |  |
| `next_approver` | `character varying(255)` | YES |  |  |
| `approved_date` | `timestamp with time zone` | YES |  |  |
| `requester_uuid` | `character varying(255)` | NO |  |  |
| `requester_name` | `character varying(255)` | NO |  |  |
| `submitted_date` | `timestamp with time zone` | NO |  |  |
| `updated_date` | `timestamp with time zone` | NO |  |  |
| `due_date` | `timestamp with time zone` | NO |  |  |
| `note` | `character varying(500)` | NO |  |  |
| `rfq_no` | `character varying(255)` | NO |  |  |
| `currency_code` | `character varying(255)` | NO |  |  |
| `currency_name` | `character varying(255)` | NO |  |  |
| `status` | `character varying(255)` | NO |  |  |
| `container_type` | `character varying(255)` | NO |  |  |
| `is_break_bulk_shipping` | `boolean` | YES |  |  |
| `dimension_length` | `double precision` | YES |  |  |
| `dimension_length_uom` | `character varying(255)` | YES |  |  |
| `dimension_breadth` | `double precision` | YES |  |  |
| `dimension_breadth_uom` | `character varying(255)` | YES |  |  |
| `dimension_height` | `double precision` | YES |  |  |
| `dimension_height_uom` | `character varying(255)` | YES |  |  |
| `volumetric` | `double precision` | YES |  |  |
| `volumetric_uom` | `character varying(255)` | YES |  |  |
| `weight` | `double precision` | NO |  |  |
| `weight_uom` | `character varying(255)` | NO |  |  |
| `hs_code` | `character varying(255)` | NO |  |  |
| `commodity` | `character varying(255)` | NO |  |  |
| `is_hazardous_goods` | `boolean` | NO |  |  |
| `msds_code` | `character varying(255)` | NO |  |  |
| `door_service_type` | `character varying(255)` | NO |  |  |
| `cargo_will_be_ready_date` | `timestamp with time zone` | NO |  |  |
| `loading_country` | `character varying(255)` | NO |  |  |
| `loading_port` | `character varying(255)` | NO |  |  |
| `loading_address` | `character varying(255)` | NO |  |  |
| `loading_address_detail` | `character varying(255)` | NO |  |  |
| `discharge_country` | `character varying(255)` | NO |  |  |
| `discharge_port` | `character varying(255)` | NO |  |  |
| `final_destination` | `character varying(255)` | NO |  |  |
| `final_destination_detail` | `character varying(255)` | NO |  |  |
| `company_name` | `character varying(255)` | YES |  |  |
| `destination_country` | `character varying(255)` | YES |  |  |
| `destination_port` | `character varying(255)` | YES |  |  |
| `loading_address_uuid` | `character varying(36)` | YES |  |  |
| `final_destination_uuid` | `character varying(36)` | YES |  |  |

#### `public.request_for_quotation_audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('request_for_quotation_audit_... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `action` | `character varying(255)` | NO |  |  |
| `date_time` | `timestamp with time zone` | NO |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `rfq_id` | `bigint(64,0)` | NO |  | FK → `public.request_for_quotation.id` |
| `supplier_company_uuid` | `character varying(255)` | YES |  |  |
| `non_vendor_id` | `bigint(64,0)` | YES |  |  |
| `upload_staff` | `character varying(100)` | YES |  |  |

**Indexes:**
- `rfq_audit_trail_pk`: `CREATE UNIQUE INDEX rfq_audit_trail_pk ON public.request_for_quotation_audit_trail USING btree (id)`

#### `public.request_for_quotation_document`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('request_for_quotation_docume... | PK |
| `guid` | `character varying(255)` | NO |  |  |
| `label` | `character varying(255)` | YES |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `description` | `character varying(255)` | YES |  |  |
| `uploaded_by` | `character varying(255)` | YES |  |  |
| `uploader_uuid` | `character varying(255)` | YES |  |  |
| `uploaded_on` | `timestamp with time zone` | NO |  |  |
| `external` | `boolean` | NO |  |  |
| `rfq_id` | `bigint(64,0)` | NO |  | FK → `public.request_for_quotation.id` |
| `supplier_company_uuid` | `character varying(255)` | YES |  |  |
| `non_vendor_id` | `bigint(64,0)` | YES |  |  |
| `upload_staff` | `character varying(100)` | YES |  |  |

#### `public.request_for_quotation_msds`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('request_for_quotation_msds_i... | PK |
| `guid` | `character varying(255)` | NO |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `rfq_id` | `bigint(64,0)` | NO |  | FK → `public.request_for_quotation.id` |

#### `public.request_for_quotation_negotiation`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('request_for_quotation_negoti... | PK |
| `user_name` | `character varying(255)` | NO |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | NO |  |  |
| `date_time` | `timestamp with time zone` | NO |  |  |
| `comment` | `character varying(500)` | YES |  |  |
| `attachment_guid` | `character varying(255)` | YES |  |  |
| `attachment_name` | `character varying(255)` | YES |  |  |
| `rfq_vendor_id` | `bigint(64,0)` | YES |  | FK → `public.rfq_vendor.id` |
| `rfq_non_vendor_id` | `bigint(64,0)` | YES |  | FK → `public.rfq_non_vendor.id` |

#### `public.request_for_quotation_ocean_freight`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('request_for_quotation_ocean_... | PK |
| `item_code` | `character varying(255)` | NO |  |  |
| `item_name` | `character varying(255)` | NO |  |  |
| `uom` | `character varying(255)` | YES |  |  |
| `currency_code` | `character varying(255)` | YES |  |  |
| `quoted_price` | `double precision` | YES |  |  |
| `quantity` | `double precision` | YES |  |  |
| `is_reefer` | `boolean` | YES |  |  |
| `remark` | `character varying(255)` | YES |  |  |
| `rfq_vendor_id` | `bigint(64,0)` | YES |  | FK → `public.rfq_vendor.id` |
| `rfq_non_vendor_id` | `bigint(64,0)` | YES |  | FK → `public.rfq_non_vendor.id` |
| `tax_code` | `character varying(255)` | YES |  |  |
| `tax_rate` | `numeric(25,12)` | YES |  |  |

#### `public.request_for_quotation_shipping_container`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('request_for_quotation_shippi... | PK |
| `item_name` | `character varying(255)` | NO |  |  |
| `quantity` | `double precision` | NO |  |  |
| `is_reefer` | `boolean` | NO |  |  |
| `rfq_id` | `bigint(64,0)` | NO |  | FK → `public.request_for_quotation.id` |
| `item_code` | `character varying(255)` | YES |  |  |
| `currency_code` | `character varying(255)` | YES |  |  |
| `uom` | `character varying(255)` | YES |  |  |

#### `public.request_for_quotation_subject_to`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('request_for_quotation_subjec... | PK |
| `item_code` | `character varying(255)` | NO |  |  |
| `item_name` | `character varying(255)` | NO |  |  |
| `uom` | `character varying(255)` | YES |  |  |
| `currency_code` | `character varying(255)` | YES |  |  |
| `quoted_price` | `double precision` | YES |  |  |
| `quantity` | `double precision` | YES |  |  |
| `remark` | `character varying(255)` | YES |  |  |
| `rfq_vendor_id` | `bigint(64,0)` | YES |  | FK → `public.rfq_vendor.id` |
| `rfq_non_vendor_id` | `bigint(64,0)` | YES |  | FK → `public.rfq_non_vendor.id` |
| `tax_code` | `character varying(255)` | YES |  |  |
| `tax_rate` | `numeric(25,12)` | YES |  |  |

#### `public.rfq_email_access`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('rfq_email_access_id_seq'::re... | PK |
| `rfq_uuid` | `character varying(255)` | YES |  |  |
| `supplier_uuid` | `character varying(255)` | YES |  |  |
| `supplier_contact_email` | `character varying(255)` | YES |  |  |
| `token` | `character varying(1000)` | YES |  |  |
| `created_at` | `timestamp with time zone` | YES |  |  |
| `expired_at` | `timestamp with time zone` | YES |  |  |
| `non_vendor_company_name` | `character varying(255)` | YES |  |  |
| `non_vendor_id` | `bigint(64,0)` | YES |  |  |
| `used` | `boolean` | YES | false |  |

**Indexes:**
- `rfq_email_access_id_uindex`: `CREATE UNIQUE INDEX rfq_email_access_id_uindex ON public.rfq_email_access USING btree (id)`
- `rfq_email_access_pk`: `CREATE UNIQUE INDEX rfq_email_access_pk ON public.rfq_email_access USING btree (id)`

#### `public.rfq_non_vendor`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('rfq_non_vendor_id_seq'::regc... | PK |
| `rfq_id` | `bigint(64,0)` | YES |  | FK → `public.request_for_quotation.id` |
| `company_name` | `character varying(255)` | NO |  |  |
| `contact_person_name` | `character varying(255)` | YES |  |  |
| `contact_person_email` | `character varying(255)` | NO |  |  |
| `validity_date` | `timestamp with time zone` | YES |  |  |
| `checked` | `boolean` | YES |  |  |
| `is_custom_clearance` | `boolean` | YES |  |  |

#### `public.rfq_quote`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('rfq_quote_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `supplier_uuid` | `character varying(255)` | YES |  |  |
| `request_for_quotation_id` | `bigint(64,0)` | YES |  | FK → `public.request_for_quotation.id` |
| `quote_time` | `integer(32,0)` | YES | 0 |  |
| `submitted_date` | `timestamp with time zone` | YES |  |  |
| `updated_date` | `timestamp with time zone` | YES |  |  |
| `rfq_non_vendor_id` | `bigint(64,0)` | YES |  |  |

**Indexes:**
- `rfq_quote_pk`: `CREATE UNIQUE INDEX rfq_quote_pk ON public.rfq_quote USING btree (id)`

#### `public.rfq_quote_item`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('rfq_quote_item_id_seq'::regc... | PK |
| `item_code` | `character varying(255)` | YES |  |  |
| `item_name` | `character varying(255)` | YES |  |  |
| `uom` | `character varying(255)` | YES |  |  |
| `currency_code` | `character varying(255)` | YES |  |  |
| `quantity` | `numeric(25,12)` | YES |  |  |
| `quoted_price` | `numeric(25,12)` | YES |  |  |
| `tax_code` | `character varying(255)` | YES |  |  |
| `tax_rate` | `numeric(25,12)` | YES |  |  |
| `is_reefer` | `boolean` | YES |  |  |
| `remark` | `character varying(255)` | YES |  |  |
| `is_ocean_freight` | `boolean` | YES | false |  |
| `quote_sequence` | `integer(32,0)` | YES | 0 |  |
| `rfq_quote_id` | `bigint(64,0)` | YES |  | FK → `public.rfq_quote.id` |
| `is_manual` | `boolean` | YES | false |  |

**Indexes:**
- `rfq_quote_item_pk`: `CREATE UNIQUE INDEX rfq_quote_item_pk ON public.rfq_quote_item USING btree (id)`

#### `public.rfq_vendor`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('rfq_vendor_id_seq'::regclass) | PK |
| `rfq_id` | `bigint(64,0)` | YES |  | FK → `public.request_for_quotation.id` |
| `vendor_id` | `bigint(64,0)` | YES |  | FK → `public.vendor.id` |
| `supplier_company_uuid` | `character varying(255)` | YES |  |  |
| `validity_date` | `timestamp with time zone` | YES |  |  |
| `checked` | `boolean` | YES |  |  |
| `is_custom_clearance` | `boolean` | YES |  |  |

#### `public.select_inbound_item`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('select_inbound_item_id_seq':... | PK |
| `inbound_request_item_id` | `bigint(64,0)` | YES |  |  |
| `inbound_request_id` | `bigint(64,0)` | YES |  | FK → `public.inbound_request.id` |

#### `public.shipping_instruction`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('shipping_instruction_id_seq'... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `created_at` | `timestamp with time zone` | NO |  |  |
| `updated_at` | `timestamp with time zone` | NO |  |  |
| `booking_no` | `character varying(255)` | YES |  |  |
| `is_original_bl` | `boolean` | YES |  |  |
| `bl_number` | `character varying(255)` | YES |  |  |
| `number` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `title` | `character varying(255)` | YES |  |  |
| `number_of_original_bl` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `requester_uuid` | `character varying(255)` | YES |  |  |
| `requester_name` | `character varying(255)` | YES |  |  |
| `feeder_vessel_name` | `character varying(255)` | YES |  |  |
| `mother_vessel` | `character varying(255)` | YES |  |  |
| `place_of_receipt` | `character varying(255)` | YES |  |  |
| `loading_port` | `character varying(255)` | YES |  |  |
| `loading_country` | `character varying(255)` | YES |  |  |
| `discharge_port` | `character varying(255)` | YES |  |  |
| `discharge_country` | `character varying(255)` | YES |  |  |
| `freight_payable` | `character varying(255)` | YES |  |  |
| `ams_scac_code` | `character varying(255)` | YES |  |  |
| `hbl_no` | `character varying(255)` | YES |  |  |
| `eta` | `timestamp with time zone` | YES |  |  |
| `etd` | `timestamp with time zone` | YES |  |  |
| `shipped_on_board` | `timestamp with time zone` | YES |  |  |
| `final_destination` | `character varying(255)` | YES |  |  |
| `shipper_name` | `character varying(255)` | YES |  |  |
| `shipper_email` | `character varying(255)` | YES |  |  |
| `shipper_phone_number` | `character varying(255)` | YES |  |  |
| `shipper_address` | `character varying(255)` | YES |  |  |
| `consignee_name` | `character varying(255)` | YES |  |  |
| `consignee_email` | `character varying(255)` | YES |  |  |
| `consignee_phone_number` | `character varying(255)` | YES |  |  |
| `consignee_address` | `character varying(255)` | YES |  |  |
| `notify_party_name` | `character varying(255)` | YES |  |  |
| `notify_party_email` | `character varying(255)` | YES |  |  |
| `notify_party_address` | `character varying(255)` | YES |  |  |
| `notify_party_phone_number` | `character varying(255)` | YES |  |  |
| `buyer_id` | `bigint(64,0)` | YES |  | FK → `public.buyer.id` |
| `vendor_id` | `bigint(64,0)` | YES |  | FK → `public.vendor.id` |
| `booking_confirmation_id` | `bigint(64,0)` | YES |  | FK → `public.booking_confirmation.id` |
| `approval_route_uuid` | `character varying(255)` | YES |  |  |
| `approval_route_name` | `character varying(255)` | YES |  |  |
| `approval_route_sequence` | `text` | YES |  |  |
| `next_approver_group_uuid` | `character varying(255)` | YES |  |  |
| `next_approver` | `character varying(255)` | YES |  |  |
| `approved_date` | `timestamp with time zone` | YES |  |  |
| `issued_at` | `timestamp with time zone` | YES |  |  |
| `submitted_at` | `timestamp with time zone` | YES |  |  |
| `destination_agent_name` | `character varying(255)` | YES |  |  |
| `destination_agent_address` | `character varying(255)` | YES |  |  |
| `destination_agent_tel` | `character varying(255)` | YES |  |  |
| `destination_agent_email` | `character varying(255)` | YES |  |  |
| `container_quantity` | `integer(32,0)` | YES |  |  |
| `final_destination_detail` | `character varying(500)` | YES |  |  |
| `shipper_dial_code` | `character varying(255)` | YES |  |  |
| `shipper_uen` | `character varying(255)` | YES |  |  |
| `consignee_dial_code` | `character varying(255)` | YES |  |  |
| `consignee_uen` | `character varying(255)` | YES |  |  |
| `consignee_same_as_shipper` | `boolean` | YES | false |  |
| `notify_party_dial_code` | `character varying(255)` | YES |  |  |
| `notify_party_uen` | `character varying(255)` | YES |  |  |
| `notify_party_same_as_consignee` | `boolean` | YES | false |  |
| `shipper_address_label` | `character varying(255)` | YES |  |  |
| `consignee_address_label` | `character varying(255)` | YES |  |  |
| `notify_party_address_label` | `character varying(255)` | YES |  |  |
| `mark_and_number` | `character varying(2000)` | YES |  |  |
| `description_of_goods` | `character varying(2000)` | YES |  |  |
| `destination_agent_dial_code` | `character varying(255)` | YES |  |  |
| `destination_agent_uen` | `character varying(255)` | YES |  |  |

#### `public.si_audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('si_audit_trail_id_seq'::regc... | PK |
| `action` | `character varying(255)` | YES |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `date_time` | `timestamp with time zone` | NO |  |  |
| `designation` | `character varying(255)` | YES |  |  |
| `remark` | `text` | YES |  |  |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `shipping_instruction_id` | `bigint(64,0)` | YES |  | FK → `public.shipping_instruction.id` |
| `house_bl_uuid` | `character varying(255)` | YES |  |  |
| `pdf_version` | `character varying(255)` | YES |  |  |

#### `public.si_container`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('si_container_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `container_no` | `character varying(255)` | YES |  |  |
| `seal_no` | `character varying(255)` | YES |  |  |
| `container_type` | `character varying(255)` | YES |  |  |
| `quantity` | `integer(32,0)` | YES | 0 |  |
| `package_type` | `character varying(255)` | NO |  |  |
| `weight_kilos` | `double precision` | NO | 0 |  |
| `measurement_cbm` | `double precision` | NO | 0 |  |
| `shipping_instruction_id` | `bigint(64,0)` | YES |  | FK → `public.shipping_instruction.id` |

#### `public.si_container_summary`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('si_container_summary_id_seq'... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `container_quantity` | `integer(32,0)` | YES |  |  |
| `marks_and_no` | `character varying(255)` | YES |  |  |
| `description_of_goods` | `character varying(255)` | YES |  |  |
| `package_type` | `character varying(255)` | YES |  |  |
| `gross_weight_kilos` | `double precision` | NO |  |  |
| `measurement_kilos` | `double precision` | NO |  |  |
| `shipping_instruction_id` | `bigint(64,0)` | YES |  | FK → `public.shipping_instruction.id` |
| `seal_no` | `character varying(255)` | YES |  |  |
| `container_no` | `character varying(255)` | YES |  |  |
| `type` | `character varying(255)` | YES |  |  |
| `container_and_seal` | `character varying(500)` | YES |  |  |

#### `public.si_document`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('si_document_id_seq'::regclass) | PK |
| `description` | `character varying(500)` | YES |  |  |
| `external` | `boolean` | YES | false |  |
| `guid` | `character varying(255)` | YES |  |  |
| `label` | `character varying(255)` | YES |  |  |
| `name` | `character varying(255)` | YES |  |  |
| `uploaded_by` | `character varying(255)` | YES |  |  |
| `uploaded_on` | `character varying(255)` | YES |  |  |
| `uploader_uuid` | `character varying(255)` | YES |  |  |
| `shipping_instruction_id` | `bigint(64,0)` | YES |  | FK → `public.shipping_instruction.id` |

#### `public.vendor`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('vendor_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `company_code` | `character varying(255)` | NO |  |  |
| `company_name` | `character varying(255)` | NO |  |  |
| `uen` | `character varying(255)` | NO |  |  |
| `country_of_origin` | `character varying(255)` | NO |  |  |
| `gst_reg_no` | `character varying(255)` | YES |  |  |
| `supplier_company_uuid` | `character varying(255)` | YES |  |  |
| `address_uuid` | `character varying(255)` | NO |  |  |
| `address_label` | `character varying(500)` | NO |  |  |
| `address_first_line` | `character varying(500)` | NO |  |  |
| `address_second_line` | `character varying(255)` | YES |  |  |
| `city` | `character varying(255)` | YES |  |  |
| `state` | `character varying(255)` | NO |  |  |
| `country` | `character varying(255)` | NO |  |  |
| `postal_code` | `character varying(255)` | NO |  |  |
| `supplier_user_uuid` | `character varying(255)` | YES |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `email` | `character varying(255)` | NO |  |  |
| `country_code` | `character varying(255)` | NO |  |  |
| `phone_number` | `character varying(255)` | NO |  |  |
| `md5_checksum` | `character varying(255)` | YES |  |  |

---

## payment

**Schemas:** public
**Total tables:** 45

### Schema: `public`

#### `public.bank_account`

- **Type:** BASE TABLE  **Rows:** 268

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('bank_account_id_seq'::regclass) | PK |
| `bank_account_no` | `character varying(100)` | YES |  |  |
| `bank_name` | `character varying(500)` | YES |  |  |
| `uuid` | `character varying(255)` | YES |  |  |
| `account_holder` | `character varying(200)` | YES |  |  |
| `branch` | `character varying(1000)` | YES |  |  |
| `swift_code` | `character varying(50)` | YES |  |  |
| `md5_checksum` | `character varying(255)` | YES |  |  |
| `bank_label` | `character varying(500)` | YES |  |  |
| `country_code` | `character varying(255)` | YES |  |  |

**Indexes:**
- `table_name_id_uindex`: `CREATE UNIQUE INDEX table_name_id_uindex ON public.bank_account USING btree (id)`
- `table_name_pk`: `CREATE UNIQUE INDEX table_name_pk ON public.bank_account USING btree (id)`

#### `public.bank_integration`

- **Type:** BASE TABLE  **Rows:** 0

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('bank_integration_id_seq'::re... | PK |
| `bank_name` | `character varying(200)` | YES |  |  |
| `branch` | `character varying(1000)` | YES |  |  |
| `swift_code` | `character varying(50)` | YES |  |  |
| `created_at` | `timestamp with time zone` | YES | now() |  |

**Indexes:**
- `bank_integration_id_uindex`: `CREATE UNIQUE INDEX bank_integration_id_uindex ON public.bank_integration USING btree (id)`
- `bank_integration_pk`: `CREATE UNIQUE INDEX bank_integration_pk ON public.bank_integration USING btree (id)`

#### `public.bank_integration_product`

- **Type:** BASE TABLE  **Rows:** 0

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('bank_integration_product_id_... | PK |
| `name` | `character varying(200)` | YES |  |  |
| `description` | `character varying(500)` | YES |  |  |
| `bank_id` | `integer(32,0)` | YES |  | FK → `public.bank_integration.id` |
| `created_at` | `timestamp with time zone` | YES | now() |  |

**Indexes:**
- `bank_integration_product_id_uindex`: `CREATE UNIQUE INDEX bank_integration_product_id_uindex ON public.bank_integration_product USING btree (id)`
- `bank_integration_product_pk`: `CREATE UNIQUE INDEX bank_integration_product_pk ON public.bank_integration_product USING btree (id)`

#### `public.bank_transaction`

- **Type:** BASE TABLE  **Rows:** 371

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('bank_transaction_id_seq'::re... | PK |
| `uuid` | `character varying(50)` | YES |  |  |
| `status` | `character varying(50)` | YES |  |  |
| `acknowledgement_id` | `bigint(64,0)` | YES |  | FK → `public.bank_transaction_acknowledgement.id` |
| `created_by_uuid` | `character varying(50)` | YES |  |  |
| `created_at` | `timestamp without time zone` | YES | now() |  |
| `updated_at` | `timestamp without time zone` | YES | now() |  |
| `mt_bank_product_id` | `bigint(64,0)` | YES |  | FK → `public.mt_bank_product.id` |
| `requested_execution_date` | `date` | YES |  |  |
| `payment_information_id` | `character varying(50)` | YES |  |  |
| `bank_account_id` | `bigint(64,0)` | YES |  | FK → `public.bank_account.id` |
| `email_list` | `ARRAY` | YES |  |  |
| `charge_bearer` | `character varying(20)` | YES |  |  |
| `payment_batch_id` | `bigint(64,0)` | YES |  | FK → `public.payment_batch.id` |
| `payment_file_name` | `character varying(500)` | YES |  |  |
| `bank_reference_number` | `character varying` | YES |  |  |

#### `public.bank_transaction_acknowledgement`

- **Type:** BASE TABLE  **Rows:** 198

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('bank_transaction_acknowledge... | PK |
| `ack_type` | `character varying(50)` | YES |  |  |
| `transaction_status` | `character varying(1000)` | YES |  |  |
| `payment_status` | `character varying(1000)` | YES |  |  |
| `bank_transaction_id` | `bigint(64,0)` | YES |  | FK → `public.bank_transaction.id` |
| `additional_info` | `character varying(255)` | YES |  |  |

#### `public.bank_transaction_running_number`

- **Type:** BASE TABLE  **Rows:** 215

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('bank_transaction_running_num... |  |
| `date` | `character varying` | YES |  |  |
| `number` | `integer(32,0)` | YES |  |  |
| `outbox_folder` | `character varying(50)` | YES |  |  |
| `bank_transaction_id` | `bigint(64,0)` | YES |  | FK → `public.bank_transaction.id` |

#### `public.beneficiary`

- **Type:** BASE TABLE  **Rows:** 1018

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('beneficiary_id_seq'::regclass) | PK |
| `supplier_code` | `character varying(50)` | YES |  |  |
| `company_name` | `character varying(255)` | YES |  |  |
| `supplier_uuid` | `character varying(255)` | YES |  |  |
| `md5_checksum` | `character varying(255)` | YES |  |  |
| `uen` | `character varying(50)` | YES |  |  |

**Indexes:**
- `beneficiary_id_uindex`: `CREATE UNIQUE INDEX beneficiary_id_uindex ON public.beneficiary USING btree (id)`
- `beneficiary_pk`: `CREATE UNIQUE INDEX beneficiary_pk ON public.beneficiary USING btree (id)`

#### `public.claim_batch_payment`

- **Type:** BASE TABLE  **Rows:** 206

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('claim_batch_payment_id_seq':... | PK |
| `payment_id` | `bigint(64,0)` | NO |  | FK → `public.payment.id` |
| `uuid` | `character varying(255)` | NO |  |  |
| `amount` | `numeric(25,2)` | YES | 0 |  |
| `nature_of_request` | `character varying(255)` | YES |  |  |
| `requester_uuid` | `character varying(255)` | YES |  |  |
| `claim_request_for` | `character varying(255)` | YES |  |  |

#### `public.credit_note`

- **Type:** BASE TABLE  **Rows:** 170

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('credit_note_id_seq'::regclass) | PK |
| `invoice_id` | `bigint(64,0)` | YES |  |  |
| `payment_id` | `bigint(64,0)` | NO |  | FK → `public.payment.id` |
| `amount` | `numeric(15,2)` | YES | 0 |  |
| `uuid` | `character varying(255)` | YES |  |  |

**Indexes:**
- `credit_note_id_uindex`: `CREATE UNIQUE INDEX credit_note_id_uindex ON public.credit_note USING btree (id)`
- `credit_note_pk`: `CREATE UNIQUE INDEX credit_note_pk ON public.credit_note USING btree (id)`

#### `public.debit_note`

- **Type:** BASE TABLE  **Rows:** 2

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('debit_note_id_seq'::regclass) | PK |
| `invoice_id` | `bigint(64,0)` | YES |  |  |
| `payment_id` | `bigint(64,0)` | NO |  | FK → `public.payment.id` |
| `amount` | `double precision` | YES | 0 |  |
| `uuid` | `character varying(255)` | YES |  |  |

**Indexes:**
- `debit_note_pk`: `CREATE UNIQUE INDEX debit_note_pk ON public.debit_note USING btree (id)`

#### `public.dummy_payment_inv_project_mapping`

- **Type:** BASE TABLE  **Rows:** 2511

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('dummy_payment_inv_project_ma... | PK |
| `payment_invoice_id` | `bigint(64,0)` | NO |  | FK → `public.invoice_payment.id` |
| `project_id` | `bigint(64,0)` | NO |  | FK → `public.project.id` |

**Indexes:**
- `uk_payment_invoice_proj`: `CREATE UNIQUE INDEX uk_payment_invoice_proj ON public.dummy_payment_inv_project_mapping USING btree (payment_invoice_id, project_id)`

#### `public.dummy_proj_invoice`

- **Type:** BASE TABLE  **Rows:** 7029

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('dummy_proj_invoice_id_seq'::... | PK |
| `invoice_uuid` | `character varying(255)` | NO |  |  |
| `project_uuid` | `character varying(255)` | NO |  |  |
| `project_code` | `character varying(255)` | YES |  |  |
| `project_title` | `character varying(255)` | YES |  |  |

#### `public.email_template`

- **Type:** BASE TABLE  **Rows:** 17

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('email_template_id_seq'::regc... | PK |
| `feature_code` | `character varying(50)` | YES |  |  |
| `action` | `character varying(50)` | YES |  |  |
| `subject` | `character varying(500)` | YES |  |  |
| `content` | `text` | YES |  |  |

**Indexes:**
- `email_template_id_uindex`: `CREATE UNIQUE INDEX email_template_id_uindex ON public.email_template USING btree (id)`
- `email_template_pk`: `CREATE UNIQUE INDEX email_template_pk ON public.email_template USING btree (id)`

#### `public.end_to_end_id_seq`

- **Type:** BASE TABLE  **Rows:** 14

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('end_to_end_id_seq_id_seq'::r... | PK |
| `seq` | `bigint(64,0)` | YES |  |  |
| `company_uuid` | `character varying(50)` | YES |  |  |

**Indexes:**
- `end_to_end_id_seq_et_bank_integration_id_key`: `CREATE UNIQUE INDEX end_to_end_id_seq_et_bank_integration_id_key ON public.end_to_end_id_seq USING btree (company_uuid)`

#### `public.entity_code`

- **Type:** BASE TABLE  **Rows:** 7

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('entity_code_id_seq'::regclass) | PK |
| `entity_uuid` | `character varying(255)` | NO |  |  |
| `entity_code` | `character varying(255)` | NO |  |  |
| `entity_name` | `character varying(255)` | YES |  |  |
| `created_on` | `timestamp with time zone` | YES |  |  |
| `updated_on` | `timestamp with time zone` | YES |  |  |
| `host_bank` | `character varying(255)` | YES |  |  |

**Indexes:**
- `entity_code_pk`: `CREATE UNIQUE INDEX entity_code_pk ON public.entity_code USING btree (id)`
- `entity_code_unique_entity_uuid_host_bank`: `CREATE UNIQUE INDEX entity_code_unique_entity_uuid_host_bank ON public.entity_code USING btree (entity_uuid, host_bank)`

#### `public.erp_api_configuration`

- **Type:** BASE TABLE  **Rows:** 12

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `company_uuid` | `character varying(100)` | NO |  |  |
| `api_type` | `character varying(250)` | NO |  |  |
| `api_url` | `character varying(250)` | NO |  |  |
| `user_name` | `character varying(100)` | YES |  |  |
| `password` | `character varying(100)` | YES |  |  |
| `id` | `integer(32,0)` | NO | nextval('erp_api_configuration_id_seq... |  |

**Indexes:**
- `erp_api_configuration_company_api_uindex`: `CREATE UNIQUE INDEX erp_api_configuration_company_api_uindex ON public.erp_api_configuration USING btree (company_uuid, api_type)`

#### `public.et_bank_integration`

- **Type:** BASE TABLE  **Rows:** 104

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO |  | PK |
| `entity_pgp_private_key` | `text` | YES |  |  |
| `entity_pgp_public_key` | `text` | YES |  |  |
| `bank_pgp_public_key` | `text` | YES |  |  |
| `bank_customer_id` | `character varying(255)` | YES |  |  |
| `s3_doxa_out_folder` | `character varying(255)` | YES |  |  |
| `s3_doxa_in_folder` | `character varying(255)` | YES |  |  |
| `file_type` | `character varying(10)` | YES | 'xml'::character varying |  |
| `out_file_suffix_encrypt_ext` | `character varying(50)` | YES |  |  |
| `description` | `character varying(500)` | YES |  |  |
| `created_by_id` | `bigint(64,0)` | YES |  |  |
| `updated_by_id` | `bigint(64,0)` | YES |  |  |
| `created_at` | `timestamp without time zone` | YES | now() |  |
| `updated_at` | `timestamp without time zone` | YES | now() |  |
| `uuid` | `character varying(255)` | YES |  |  |
| `mt_bank_product_id` | `bigint(64,0)` | YES |  | FK → `public.mt_bank_product.id` |
| `bank_integration_name` | `character varying(50)` | YES |  |  |
| `sub_org_id` | `character varying(50)` | YES |  |  |
| `pass_phrase` | `character varying(100)` | YES |  |  |
| `host_bank` | `character varying(50)` | YES |  |  |
| `bank_account_uuid` | `character varying(255)` | YES |  |  |

#### `public.et_bank_integration_email`

- **Type:** BASE TABLE  **Rows:** 0

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('et_bank_integration_email_id... | PK |
| `email` | `character varying(255)` | NO |  |  |
| `company_uuid` | `character varying(50)` | NO |  |  |
| `is_deleted` | `boolean` | YES | false |  |
| `created_at` | `timestamp without time zone` | YES | now() |  |
| `updated_at` | `timestamp without time zone` | YES | now() |  |

**Indexes:**
- `et_bank_integration_email_email_entity_id_uindex`: `CREATE UNIQUE INDEX et_bank_integration_email_email_entity_id_uindex ON public.et_bank_integration_email USING btree (company_uuid, email)`

#### `public.invoice_payment`

- **Type:** BASE TABLE  **Rows:** 3456

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('invoice_payment_id_seq'::reg... | PK |
| `payment_id` | `bigint(64,0)` | NO |  | FK → `public.payment.id` |
| `uuid` | `character varying(255)` | NO |  |  |
| `amount` | `numeric(15,2)` | YES | 0 |  |
| `project_code` | `character varying(255)` | YES |  |  |
| `invoice_type` | `character varying(50)` | YES |  |  |
| `nature_of_invoice` | `character varying(100)` | YES |  |  |

**Indexes:**
- `invoice_payment_id_uindex`: `CREATE UNIQUE INDEX invoice_payment_id_uindex ON public.invoice_payment USING btree (id)`
- `invoice_payment_pk`: `CREATE UNIQUE INDEX invoice_payment_pk ON public.invoice_payment USING btree (id)`

#### `public.invoice_payment_details_view`

- **Type:** VIEW  **Rows:** —

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `batchdate` | `timestamp with time zone` | YES |  |  |
| `description` | `text` | YES |  |  |
| `invoiceuuid` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |

#### `public.liquibase-changelog`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `character varying(255)` | NO |  |  |
| `author` | `character varying(255)` | NO |  |  |
| `filename` | `character varying(255)` | NO |  |  |
| `dateexecuted` | `timestamp without time zone` | NO |  |  |
| `orderexecuted` | `integer(32,0)` | NO |  |  |
| `exectype` | `character varying(10)` | NO |  |  |
| `md5sum` | `character varying(35)` | YES |  |  |
| `description` | `character varying(255)` | YES |  |  |
| `comments` | `character varying(255)` | YES |  |  |
| `tag` | `character varying(255)` | YES |  |  |
| `liquibase` | `character varying(20)` | YES |  |  |
| `contexts` | `character varying(255)` | YES |  |  |
| `labels` | `character varying(255)` | YES |  |  |
| `deployment_id` | `character varying(10)` | YES |  |  |

#### `public.liquibase-lock`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO |  | PK |
| `locked` | `boolean` | NO |  |  |
| `lockgranted` | `timestamp without time zone` | YES |  |  |
| `lockedby` | `character varying(255)` | YES |  |  |

**Indexes:**
- `LIQUIBASE-LOCK_PKEY`: `CREATE UNIQUE INDEX "LIQUIBASE-LOCK_PKEY" ON public."liquibase-lock" USING btree (id)`

#### `public.mt_bank`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `code` | `character varying(255)` | NO |  | PK |
| `created_on` | `timestamp without time zone` | YES |  |  |
| `updated_on` | `timestamp without time zone` | YES |  |  |
| `name` | `character varying(255)` | YES |  |  |
| `mt_country_iso_code` | `character varying(255)` | YES |  |  |

#### `public.mt_bank_product`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('mt_bank_product_id_seq'::reg... | PK |
| `mt_bank_code` | `character varying` | YES |  |  |
| `product_type` | `character varying(50)` | NO |  |  |
| `product_desc` | `character varying(255)` | NO |  |  |
| `xml_filename_prefix` | `character varying(50)` | YES |  |  |
| `xml_filename_suffix` | `character varying(50)` | YES |  |  |
| `is_active` | `boolean` | YES | true |  |
| `created_at` | `timestamp without time zone` | YES | now() |  |
| `updated_at` | `timestamp without time zone` | YES | now() |  |
| `host_bank` | `character varying(20)` | NO |  |  |
| `product_group_code` | `character varying(50)` | YES |  |  |
| `product_group_name` | `character varying(255)` | YES |  |  |
| `product_type_control_execution_date` | `character varying(255)` | YES |  |  |

#### `public.payment`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('payment_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `payment_number` | `character varying(50)` | YES |  |  |
| `ref_number` | `character varying(500)` | YES |  |  |
| `currency` | `character varying(20)` | YES |  |  |
| `approval_route_uuid` | `character varying(255)` | YES |  |  |
| `approval_sequence` | `character varying(1000)` | YES |  |  |
| `approval_name` | `character varying(1000)` | YES |  |  |
| `next_approval_group` | `character varying(500)` | YES |  |  |
| `next_approval_group_uuid` | `character varying(255)` | YES |  |  |
| `status` | `character varying(50)` | NO |  |  |
| `inv_amount` | `numeric(15,2)` | YES | 0 |  |
| `cn_amount` | `numeric(15,2)` | YES | 0 |  |
| `total_amount` | `numeric(15,2)` | YES | 0 |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `created_by` | `character varying(255)` | YES |  |  |
| `created_by_uuid` | `character varying(255)` | YES |  |  |
| `beneficiary_id` | `bigint(64,0)` | NO | nextval('payment_beneficiary_id_seq':... | FK → `public.beneficiary.id` |
| `created_at` | `timestamp with time zone` | YES |  |  |
| `remarks` | `character varying(1000)` | YES |  |  |
| `approved_at` | `timestamp with time zone` | YES |  |  |
| `released_at` | `timestamp with time zone` | YES |  |  |
| `payment_batch_created` | `boolean` | YES | false |  |
| `earliest_sys_due_date` | `timestamp with time zone` | YES |  |  |
| `currency_name` | `character varying(50)` | YES |  |  |
| `payment_type` | `character varying(20)` | YES | 'P2P'::character varying |  |
| `dn_amount` | `numeric(15,2)` | YES |  |  |
| `root_uuids` | `text` | YES |  |  |
| `updated_at` | `timestamp with time zone` | YES | now() |  |
| `earliest_inv_due_date` | `timestamp with time zone` | YES |  |  |
| `bc_amount` | `double precision` | YES | 0 |  |
| `claim_batch_amount` | `numeric(25,2)` | YES | 0 |  |
| `payment_origin` | `character varying(255)` | YES |  |  |

**Indexes:**
- `payment_id_uindex`: `CREATE UNIQUE INDEX payment_id_uindex ON public.payment USING btree (id)`
- `payment_number_companyuuid_unique_index`: `CREATE UNIQUE INDEX payment_number_companyuuid_unique_index ON public.payment USING btree (payment_number, company_uuid)`
- `payment_pk`: `CREATE UNIQUE INDEX payment_pk ON public.payment USING btree (id)`

#### `public.payment_audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('payment_audit_trail_id_seq':... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_role` | `character varying(500)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `action` | `character varying(255)` | YES |  |  |
| `remarks` | `character varying(500)` | YES |  |  |
| `date_time` | `timestamp with time zone` | YES |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `payment_id` | `bigint(64,0)` | NO | nextval('payment_audit_trail_payment_... |  |

**Indexes:**
- `payment_audit_trail_id_uindex`: `CREATE UNIQUE INDEX payment_audit_trail_id_uindex ON public.payment_audit_trail USING btree (id)`
- `payment_audit_trail_pk`: `CREATE UNIQUE INDEX payment_audit_trail_pk ON public.payment_audit_trail USING btree (id)`

#### `public.payment_back_charge`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('payment_back_charge_id_seq':... | PK |
| `payment_id` | `bigint(64,0)` | NO |  | FK → `public.payment.id` |
| `invoice_id` | `bigint(64,0)` | YES |  |  |
| `uuid` | `character varying(255)` | NO |  |  |
| `amount` | `double precision` | YES | 0 |  |
| `project_code` | `character varying(255)` | YES |  |  |

**Indexes:**
- `payment_back_charge_id_uindex`: `CREATE UNIQUE INDEX payment_back_charge_id_uindex ON public.payment_back_charge USING btree (id)`

#### `public.payment_batch`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('payment_batch_id_seq'::regcl... | PK |
| `payment_batch_number` | `character varying(255)` | YES |  |  |
| `uuid` | `character varying(255)` | YES |  |  |
| `reference_number` | `character varying(500)` | YES |  |  |
| `currency` | `character varying(20)` | YES |  |  |
| `status` | `character varying(50)` | YES |  |  |
| `transfer_status` | `character varying(50)` | YES |  |  |
| `payment_release_date` | `timestamp with time zone` | YES |  |  |
| `executed_date` | `timestamp with time zone` | YES |  |  |
| `remarks` | `character varying(500)` | YES |  |  |
| `created_by` | `character varying(100)` | YES |  |  |
| `total_amount` | `numeric(15,2)` | YES | 0 |  |
| `created_by_uuid` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `source_bank_account_id` | `integer(32,0)` | YES |  | FK → `public.bank_account.id` |
| `bank_integration_product_id` | `integer(32,0)` | YES |  | FK → `public.bank_integration_product.id` |
| `created_at` | `timestamp with time zone` | YES |  |  |
| `payment_method` | `character varying(50)` | YES |  |  |
| `cheque_number` | `character varying(200)` | YES |  |  |
| `email_list` | `ARRAY` | YES |  |  |
| `sort_code` | `character varying(50)` | YES |  |  |

**Indexes:**
- `payment_batch_document_metadata_id_uindex`: `CREATE UNIQUE INDEX payment_batch_document_metadata_id_uindex ON public.payment_batch USING btree (id)`
- `payment_batch_id_uindex`: `CREATE UNIQUE INDEX payment_batch_id_uindex ON public.payment_batch USING btree (id)`
- `payment_batch_number_companyuuid_unique_index`: `CREATE UNIQUE INDEX payment_batch_number_companyuuid_unique_index ON public.payment_batch USING btree (payment_batch_number, company_uuid)`
- `payment_batch_pk`: `CREATE UNIQUE INDEX payment_batch_pk ON public.payment_batch USING btree (id)`

#### `public.payment_batch_audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('payment_batch_audit_trail_id... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_role` | `character varying(500)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `action` | `character varying(255)` | YES |  |  |
| `remarks` | `character varying(500)` | YES |  |  |
| `date_time` | `timestamp with time zone` | YES |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `payment_batch_id` | `bigint(64,0)` | NO |  | FK → `public.payment_batch.id` |

**Indexes:**
- `payment_batch_audit_trail_id_uindex`: `CREATE UNIQUE INDEX payment_batch_audit_trail_id_uindex ON public.payment_batch_audit_trail USING btree (id)`
- `payment_batch_audit_trail_pk`: `CREATE UNIQUE INDEX payment_batch_audit_trail_pk ON public.payment_batch_audit_trail USING btree (id)`

#### `public.payment_batch_document`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('payment_batch_document_id_se... | PK |
| `guid` | `character varying(255)` | YES |  |  |
| `file_label` | `character varying(255)` | YES |  |  |
| `file_description` | `character varying(500)` | YES |  |  |
| `uploaded_on` | `timestamp with time zone` | YES |  |  |
| `uploaded_by_name` | `character varying(255)` | YES |  |  |
| `uploaded_by_uuid` | `character varying(255)` | YES |  |  |
| `payment_batch_id` | `bigint(64,0)` | NO | nextval('payment_batch_document_payme... | FK → `public.payment_batch.id` |
| `attachment` | `character varying(255)` | YES |  |  |
| `file_name` | `character varying(255)` | YES |  |  |

**Indexes:**
- `payment_batch_document_metadata_pk`: `CREATE UNIQUE INDEX payment_batch_document_metadata_pk ON public.payment_batch_document USING btree (id)`

#### `public.payment_batch_item`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('payment_batch_item_id_seq'::... | PK |
| `payment_id` | `integer(32,0)` | NO |  | FK → `public.payment.id` |
| `payment_batch_id` | `integer(32,0)` | YES |  | FK → `public.payment_batch.id` |
| `receive_bank_account_id` | `integer(32,0)` | YES |  | FK → `public.bank_account.id` |
| `end_to_end_id` | `character varying(50)` | YES |  |  |
| `cheque_number` | `character varying(255)` | YES |  |  |
| `source_bank_account_id` | `integer(32,0)` | YES |  | FK → `public.bank_account.id` |

**Indexes:**
- `payment_batch_item_id_uindex`: `CREATE UNIQUE INDEX payment_batch_item_id_uindex ON public.payment_batch_item USING btree (id)`
- `payment_batch_item_pk`: `CREATE UNIQUE INDEX payment_batch_item_pk ON public.payment_batch_item USING btree (id)`

#### `public.payment_batch_view`

- **Type:** VIEW  **Rows:** —

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `payment_batch_number` | `character varying(255)` | YES |  |  |
| `payment_id` | `integer(32,0)` | YES |  |  |
| `payment_batch_id` | `integer(32,0)` | YES |  |  |
| `paymentcode` | `character varying(50)` | YES |  |  |
| `checknumber` | `text` | YES |  |  |
| `paymentdescription` | `text` | YES |  |  |
| `reference_number` | `character varying(500)` | YES |  |  |
| `source_bank_account_id` | `integer(32,0)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `bank` | `text` | YES |  |  |
| `bank_name` | `character varying(500)` | YES |  |  |
| `bank_id` | `integer(32,0)` | YES |  |  |

#### `public.payment_claim_batch_project_mapping`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('payment_claim_batch_project_... | PK |
| `claim_batch_payment_id` | `bigint(64,0)` | NO |  | FK → `public.claim_batch_payment.id` |
| `project_id` | `bigint(64,0)` | NO |  | FK → `public.project.id` |

#### `public.payment_details_view`

- **Type:** VIEW  **Rows:** —

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `batchselector` | `text` | YES |  |  |
| `paymentid` | `bigint(64,0)` | YES |  |  |
| `status` | `character varying(50)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `batchdate` | `timestamp with time zone` | YES |  |  |
| `headerdescription` | `text` | YES |  |  |
| `accountset` | `character varying(20)` | YES |  |  |
| `reference` | `character varying(500)` | YES |  |  |
| `checkprintrequired` | `text` | YES |  |  |
| `entrydescription` | `text` | YES |  |  |
| `paymenttransactiontype` | `text` | YES |  |  |
| `paymentamount` | `numeric(15,2)` | YES |  |  |
| `invoiceuuid` | `character varying(255)` | YES |  |  |

#### `public.payment_document_metadata`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('payment_document_metadata_id... | PK |
| `guid` | `character varying(255)` | YES |  |  |
| `file_label` | `character varying(255)` | YES |  |  |
| `attachment` | `character varying(255)` | YES |  |  |
| `file_description` | `character varying(500)` | YES |  |  |
| `uploaded_on` | `timestamp with time zone` | YES |  |  |
| `uploaded_by_name` | `character varying(255)` | YES |  |  |
| `uploaded_by_uuid` | `character varying(255)` | YES |  |  |
| `payment_id` | `bigint(64,0)` | NO | nextval('payment_document_metadata_pa... | FK → `public.payment.id` |
| `file_name` | `character varying(255)` | YES |  |  |

**Indexes:**
- `payment_document_metadata_id_uindex`: `CREATE UNIQUE INDEX payment_document_metadata_id_uindex ON public.payment_document_metadata USING btree (id)`
- `payment_document_metadata_pk`: `CREATE UNIQUE INDEX payment_document_metadata_pk ON public.payment_document_metadata USING btree (id)`

#### `public.payment_info_id_sequence`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('payment_info_id_sequence_id_... | PK |
| `sequence_number` | `character varying(5)` | YES |  |  |
| `requested_execution_date` | `date` | YES |  |  |
| `is_deleted` | `boolean` | YES | false |  |
| `company_uuid` | `character varying(50)` | YES |  |  |

#### `public.payment_inv_project_mapping`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('payment_inv_project_mapping_... | PK |
| `payment_invoice_id` | `bigint(64,0)` | NO |  | FK → `public.invoice_payment.id` |
| `project_id` | `bigint(64,0)` | NO |  | FK → `public.project.id` |

#### `public.project`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('project_id_seq'::regclass) | PK |
| `project_uuid` | `character varying(100)` | YES |  |  |
| `project_code` | `character varying(50)` | YES |  |  |
| `project_title` | `character varying(200)` | YES |  |  |

**Indexes:**
- `uk_project_project_uuid`: `CREATE UNIQUE INDEX uk_project_project_uuid ON public.project USING btree (project_uuid)`

#### `public.project_dummy`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('project_dummy_id_seq'::regcl... | PK |
| `project_uuid` | `character varying(255)` | NO |  |  |
| `project_code` | `character varying(255)` | YES |  |  |
| `project_title` | `text` | YES |  |  |

#### `public.public_holidays`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('public_holidays_id_seq'::reg... | PK |
| `holiday_name` | `character varying(255)` | YES |  |  |
| `holiday_date` | `date` | NO |  |  |
| `country` | `character varying(100)` | YES |  |  |
| `country_code` | `character varying(50)` | YES |  |  |

#### `public.tradeline_ack_file_l4`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('tradeline_ack_file_id_seq'::... | PK |
| `invoice_flag` | `character varying(50)` | YES |  |  |
| `operation` | `character varying(50)` | YES |  |  |
| `invoice_number` | `character varying(100)` | YES |  |  |
| `invoice_date` | `date` | YES |  |  |
| `invoice_due_date` | `date` | YES |  |  |
| `invoice_currency` | `character varying(10)` | YES |  |  |
| `invoice_amount` | `numeric(19,2)` | YES |  |  |
| `seller_erp_id` | `character varying(100)` | YES |  |  |
| `buyer_erp_id` | `character varying(100)` | YES |  |  |
| `relationship_id` | `character varying(100)` | YES |  |  |
| `date` | `date` | YES |  |  |
| `file_name` | `character varying(255)` | YES |  |  |

#### `public.tradeline_bank_transaction`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('tradeline_bank_transaction_i... | PK |
| `uuid` | `character varying(50)` | YES |  |  |
| `status` | `character varying(50)` | YES |  |  |
| `withdrawal_uuid` | `character varying` | YES |  |  |
| `payment_file_name` | `character varying` | YES |  |  |

#### `public.tradeline_bank_transaction_ack`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('tradeline_bank_transaction_a... | PK |
| `ack_type` | `character varying(50)` | YES |  |  |
| `transaction_status` | `character varying(1000)` | YES |  |  |
| `payment_status` | `character varying(1000)` | YES |  |  |
| `tradeline_bank_transaction_id` | `bigint(64,0)` | YES |  | FK → `public.tradeline_bank_transaction.id` |
| `additional_info` | `character varying(255)` | YES |  |  |

#### `public.tradeline_bank_transaction_running_no`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('tradeline_bank_transaction_r... |  |
| `date` | `character varying` | YES |  |  |
| `number` | `integer(32,0)` | YES |  |  |
| `outbox_folder` | `character varying(50)` | YES |  |  |
| `tradeline_bank_transaction_id` | `bigint(64,0)` | YES |  | FK → `public.tradeline_bank_transaction.id` |

#### `public.tradeline_et_bank_integration`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO |  | PK |
| `entity_pgp_private_key` | `text` | YES |  |  |
| `entity_pgp_public_key` | `text` | YES |  |  |
| `bank_pgp_public_key` | `text` | YES |  |  |
| `bank_customer_id` | `character varying(255)` | YES |  |  |
| `s3_doxa_out_folder` | `character varying(255)` | YES |  |  |
| `s3_doxa_in_folder` | `character varying(255)` | YES |  |  |
| `file_type` | `character varying(10)` | YES | 'xml'::character varying |  |
| `out_file_suffix_encrypt_ext` | `character varying(50)` | YES |  |  |
| `description` | `character varying(500)` | YES |  |  |
| `created_by_id` | `bigint(64,0)` | YES |  |  |
| `updated_by_id` | `bigint(64,0)` | YES |  |  |
| `created_at` | `timestamp without time zone` | YES | now() |  |
| `updated_at` | `timestamp without time zone` | YES | now() |  |
| `uuid` | `character varying(255)` | YES |  |  |
| `bank_integration_name` | `character varying(50)` | YES |  |  |
| `sub_org_id` | `character varying(50)` | YES |  |  |
| `pass_phrase` | `character varying(100)` | YES |  |  |
| `host_bank` | `character varying(50)` | YES |  |  |

---

## progressive-claim 1

**Schemas:** public
**Total tables:** 72

### Schema: `public`

#### `public.address`

- **Type:** BASE TABLE  **Rows:** 602

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('address_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `address_label` | `character varying(500)` | YES |  |  |
| `address_first_line` | `character varying(500)` | YES |  |  |
| `address_second_line` | `character varying(500)` | YES |  |  |
| `city` | `character varying(100)` | YES |  |  |
| `state` | `character varying(100)` | YES |  |  |
| `country` | `character varying(100)` | YES |  |  |
| `postal_code` | `character varying(20)` | YES |  |  |
| `md5_checksum` | `character varying(255)` | NO |  |  |

#### `public.approval_matrix`

- **Type:** BASE TABLE  **Rows:** 4453

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('approval_route_id_seq'::regc... | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `code` | `character varying(255)` | NO |  |  |
| `sequence` | `character varying(500)` | NO |  |  |
| `next_group_uuid` | `character varying(255)` | YES |  |  |
| `next_group_name` | `character varying(500)` | YES |  |  |

#### `public.back_charge`

- **Type:** BASE TABLE  **Rows:** 681

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('back_charge_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `number` | `character varying(255)` | NO |  |  |
| `status` | `character varying(100)` | NO |  |  |
| `work_order_id` | `bigint(64,0)` | NO |  | FK → `public.work_order.id` |
| `title` | `character varying(500)` | YES |  |  |
| `bc_reference_number` | `character varying(255)` | YES |  |  |
| `remarks` | `character varying(2000)` | YES |  |  |
| `bc_date` | `timestamp with time zone` | YES |  |  |
| `total_amount` | `double precision` | NO | 0 |  |
| `project_id` | `integer(32,0)` | YES |  | FK → `public.project.id` |
| `approval_route_id` | `integer(32,0)` | YES |  | FK → `public.approval_matrix.id` |
| `project_trade` | `character varying(255)` | YES |  |  |
| `created_by_id` | `integer(32,0)` | NO |  | FK → `public.person.id` |
| `created_at` | `timestamp with time zone` | NO |  |  |
| `vendor_id` | `bigint(64,0)` | YES |  | FK → `public.vendor.id` |
| `buyer_id` | `bigint(64,0)` | YES |  | FK → `public.buyer.id` |
| `updated_at` | `timestamp with time zone` | YES |  |  |
| `progressive_claim_id` | `bigint(64,0)` | YES |  | FK → `public.progressive_claim.id` |
| `cumulative_release` | `double precision` | YES | 0 |  |
| `balance` | `double precision` | YES | 0 |  |
| `tax_code` | `character varying(100)` | YES | NULL::character varying |  |
| `tax_amt` | `double precision` | YES | 0 |  |
| `migration_back_charge_deduction_refund_id` | `bigint(64,0)` | YES |  | FK → `public.migration_back_charge_deduction_refund.id` |
| `forecast_trade_uuid` | `character varying(255)` | YES |  |  |
| `forecast_trade_label` | `character varying(255)` | YES |  |  |
| `tax_uuid` | `character varying` | YES |  |  |
| `tax_percentage` | `double precision` | YES | 0 |  |
| `applied_in_payment` | `boolean` | YES | false |  |

**Indexes:**
- `back_charge_company_uuid_index`: `CREATE INDEX back_charge_company_uuid_index ON public.back_charge USING btree (company_uuid)`
- `back_charge_status_index`: `CREATE INDEX back_charge_status_index ON public.back_charge USING btree (status)`
- `back_charge_uuid_index`: `CREATE INDEX back_charge_uuid_index ON public.back_charge USING btree (uuid)`

#### `public.back_charge_item`

- **Type:** BASE TABLE  **Rows:** 1913

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('back_charge_item_id_seq'::re... | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `back_charge_id` | `integer(32,0)` | YES |  | FK → `public.back_charge.id` |
| `item_group` | `character varying(100)` | NO |  |  |
| `work_code` | `character varying(255)` | NO |  |  |
| `description` | `character varying(2000)` | YES |  |  |
| `uom` | `character varying(25)` | YES |  |  |
| `retention` | `boolean` | YES | false |  |
| `lump_sum` | `boolean` | YES | false |  |
| `weightage` | `double precision` | YES | 0 |  |
| `quantity` | `double precision` | YES | 0 |  |
| `unit_price` | `double precision` | YES | 0 |  |
| `total_amount` | `double precision` | YES | 0 |  |
| `remark` | `text` | YES |  |  |
| `parent_id` | `integer(32,0)` | YES |  | FK → `public.back_charge_item.id` |
| `tax_code` | `character varying(100)` | YES | NULL::character varying |  |
| `tax_percentage` | `double precision` | YES | 0 |  |
| `parent_uuid` | `character varying(255)` | YES |  |  |
| `have_children` | `boolean` | YES | false |  |
| `tax_amt` | `double precision` | YES |  |  |
| `uom_uuid` | `character varying` | YES |  |  |
| `gl_account` | `character varying(255)` | YES |  |  |

#### `public.bc_audit_trail`

- **Type:** BASE TABLE  **Rows:** 885

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('bc_audit_trail_id_seq'::regc... | PK |
| `back_charge_id` | `integer(32,0)` | YES |  | FK → `public.back_charge.id` |
| `user_name` | `character varying(255)` | NO |  |  |
| `user_uuid` | `character varying(255)` | NO |  |  |
| `designation` | `character varying(255)` | YES |  |  |
| `action` | `character varying(50)` | NO |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `date_time` | `timestamp with time zone` | NO |  |  |
| `remark` | `text` | YES |  |  |

#### `public.bc_document`

- **Type:** BASE TABLE  **Rows:** 8

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('bc_document_id_seq'::regclass) | PK |
| `guid` | `character varying(255)` | NO |  |  |
| `label` | `character varying(255)` | NO |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `description` | `character varying(255)` | NO |  |  |
| `uploaded_by` | `character varying(255)` | NO |  |  |
| `uploader_uuid` | `character varying(255)` | NO |  |  |
| `uploaded_on` | `character varying(255)` | NO |  |  |
| `external` | `boolean` | YES | false |  |
| `back_charge_id` | `bigint(64,0)` | NO |  | FK → `public.back_charge.id` |

#### `public.buyer`

- **Type:** BASE TABLE  **Rows:** 656

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('buyer_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `code` | `character varying(50)` | NO |  |  |
| `country` | `character varying(50)` | NO |  |  |
| `gst_no` | `character varying(50)` | YES |  |  |
| `company_reg_no` | `character varying(50)` | YES |  |  |
| `uen` | `character varying(50)` | NO |  |  |
| `md5_checksum` | `character varying(255)` | NO |  |  |
| `person_id` | `bigint(64,0)` | YES |  | FK → `public.person.id` |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `address_id` | `bigint(64,0)` | YES |  | FK → `public.address.id` |

#### `public.currency`

- **Type:** BASE TABLE  **Rows:** 114

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('currency_id_seq'::regclass) | PK |
| `name` | `character varying(255)` | NO |  |  |
| `code` | `character varying(50)` | NO |  |  |
| `exchange_rate` | `double precision` | NO | 1 |  |
| `uuid` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | NO |  |  |

#### `public.email_template`

- **Type:** BASE TABLE  **Rows:** 49

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('email_template_id_seq'::regc... | PK |
| `feature_code` | `character varying(50)` | YES |  |  |
| `action` | `character varying(50)` | YES |  |  |
| `subject` | `character varying(500)` | YES |  |  |
| `content` | `character varying` | YES |  |  |

**Indexes:**
- `email_template_id_uindex`: `CREATE UNIQUE INDEX email_template_id_uindex ON public.email_template USING btree (id)`
- `email_template_pk`: `CREATE UNIQUE INDEX email_template_pk ON public.email_template USING btree (id)`

#### `public.erp_api_configuration`

- **Type:** BASE TABLE  **Rows:** 2

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `company_uuid` | `character varying(100)` | NO |  |  |
| `api_type` | `character varying(250)` | NO |  |  |
| `api_url` | `character varying(250)` | NO |  |  |
| `user_name` | `character varying(100)` | YES |  |  |
| `password` | `character varying(100)` | YES |  |  |
| `id` | `integer(32,0)` | NO | nextval('erp_api_configuration_id_seq... |  |

**Indexes:**
- `erp_api_configuration_company_api_type_idx`: `CREATE UNIQUE INDEX erp_api_configuration_company_api_type_idx ON public.erp_api_configuration USING btree (company_uuid, api_type)`

#### `public.liquibase-changelog`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `character varying(255)` | NO |  |  |
| `author` | `character varying(255)` | NO |  |  |
| `filename` | `character varying(255)` | NO |  |  |
| `dateexecuted` | `timestamp without time zone` | NO |  |  |
| `orderexecuted` | `integer(32,0)` | NO |  |  |
| `exectype` | `character varying(10)` | NO |  |  |
| `md5sum` | `character varying(35)` | YES |  |  |
| `description` | `character varying(255)` | YES |  |  |
| `comments` | `character varying(255)` | YES |  |  |
| `tag` | `character varying(255)` | YES |  |  |
| `liquibase` | `character varying(20)` | YES |  |  |
| `contexts` | `character varying(255)` | YES |  |  |
| `labels` | `character varying(255)` | YES |  |  |
| `deployment_id` | `character varying(10)` | YES |  |  |

#### `public.liquibase-lock`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO |  | PK |
| `locked` | `boolean` | NO |  |  |
| `lockgranted` | `timestamp without time zone` | YES |  |  |
| `lockedby` | `character varying(255)` | YES |  |  |

#### `public.migration_audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('migration_audit_trail_id_seq... | PK |
| `sub_con_migration_id` | `bigint(64,0)` | YES |  | FK → `public.sub_con_migration.id` |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `action` | `character varying(50)` | YES |  |  |
| `designation` | `character varying(255)` | YES |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `date_time` | `timestamp with time zone` | YES |  |  |
| `remark` | `text` | YES |  |  |

**Indexes:**
- `migration_audit_trail_id_uindex`: `CREATE UNIQUE INDEX migration_audit_trail_id_uindex ON public.migration_audit_trail USING btree (id)`
- `migration_audit_trail_pk`: `CREATE UNIQUE INDEX migration_audit_trail_pk ON public.migration_audit_trail USING btree (id)`

#### `public.migration_back_charge`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('migration_back_charge_id_seq... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `bc_system_number` | `character varying(255)` | YES |  |  |
| `bc_reference_number` | `character varying(255)` | YES |  |  |
| `bc_title` | `character varying(500)` | YES |  |  |
| `bc_date` | `timestamp with time zone` | YES |  |  |
| `approval_route_id` | `bigint(64,0)` | YES |  |  |
| `gst_code` | `character varying(255)` | YES |  |  |
| `gst_percentage` | `double precision` | YES | 0 |  |
| `upload_guid` | `character varying(255)` | YES |  |  |
| `upload_file_name` | `character varying(255)` | YES |  |  |
| `sub_con_migration_id` | `bigint(64,0)` | YES |  | FK → `public.sub_con_migration.id` |
| `upload_bc_deduction_refund_file_name` | `character varying(255)` | YES |  |  |
| `upload_bc_deduction_refund_guid` | `character varying(255)` | YES |  |  |
| `bc_refund_release_amt` | `double precision` | YES | 0 |  |
| `bc_deduction_release_amt` | `double precision` | YES | 0 |  |
| `gst_for_bc_deduction` | `double precision` | YES | 0 |  |
| `gst_for_bc_refund` | `double precision` | YES | 0 |  |
| `bc_uuid` | `character varying(255)` | YES |  |  |
| `tax_uuid` | `character varying` | YES |  |  |

**Indexes:**
- `migration_back_charge_id_uindex`: `CREATE UNIQUE INDEX migration_back_charge_id_uindex ON public.migration_back_charge USING btree (id)`
- `migration_back_charge_pk`: `CREATE UNIQUE INDEX migration_back_charge_pk ON public.migration_back_charge USING btree (id)`

#### `public.migration_back_charge_deduction_refund`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('migration_back_charge_deduct... | PK |
| `upload_bc_deduction_refund_file_name` | `character varying(255)` | YES |  |  |
| `upload_bc_deduction_refund_guid` | `character varying(255)` | YES |  |  |
| `uuid` | `character varying(255)` | YES |  |  |

**Indexes:**
- `bc_deduction_rf_pk`: `CREATE UNIQUE INDEX bc_deduction_rf_pk ON public.migration_back_charge_deduction_refund USING btree (id)`

#### `public.migration_break_down`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('migration_break_down_id_seq'... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `sub_con_migration_id` | `bigint(64,0)` | YES |  | FK → `public.sub_con_migration.id` |
| `sub_contract_amt` | `double precision` | YES | 0 |  |
| `sub_contract_claim_amt` | `double precision` | YES | 0 |  |
| `sub_contract_response_amt` | `double precision` | YES | 0 |  |
| `sub_vr_claim_amt` | `double precision` | YES | 0 |  |
| `sub_vr_response_amt` | `double precision` | YES | 0 |  |
| `total_contract_amt` | `double precision` | YES | 0 |  |
| `total_claim_amt` | `double precision` | YES | 0 |  |
| `total_response_amt` | `double precision` | YES | 0 |  |
| `subcon_vr_claim_amt_with_retention` | `double precision` | YES | 0 |  |
| `original_contract_claim_amt_with_retention` | `double precision` | YES | 0 |  |
| `mos_claim_amt_with_retention` | `double precision` | YES | 0 |  |
| `subcon_vr_response_amt_with_retention` | `double precision` | YES | 0 |  |
| `original_contract_response_amt_with_retention` | `double precision` | YES | 0 |  |
| `mos_response_amt_with_retention` | `double precision` | YES | 0 |  |
| `subcon_vr_response_amt_added_to_retention_cap` | `double precision` | YES | 0 |  |
| `subcon_vr_claim_amt_added_to_retention_cap` | `double precision` | YES | 0 |  |

**Indexes:**
- `migration_break_down_id_uindex`: `CREATE UNIQUE INDEX migration_break_down_id_uindex ON public.migration_break_down USING btree (id)`
- `migration_break_down_pk`: `CREATE UNIQUE INDEX migration_break_down_pk ON public.migration_break_down USING btree (id)`

#### `public.migration_items_record`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('migration_items_record_id_se... | PK |
| `sub_type` | `character varying(255)` | YES |  |  |
| `description` | `text` | YES |  |  |
| `amount` | `double precision` | YES | 0 |  |
| `release_amt` | `double precision` | YES | 0 |  |
| `sub_con_migration_id` | `bigint(64,0)` | YES |  | FK → `public.sub_con_migration.id` |
| `is_release` | `boolean` | YES | false |  |
| `release_description` | `text` | YES |  |  |
| `bc_uuid` | `character varying(255)` | YES |  |  |

**Indexes:**
- `migration_items_record_id_uindex`: `CREATE UNIQUE INDEX migration_items_record_id_uindex ON public.migration_items_record USING btree (id)`
- `migration_items_record_pk`: `CREATE UNIQUE INDEX migration_items_record_pk ON public.migration_items_record USING btree (id)`

#### `public.migration_main_con_variation`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('migration_main_con_variation... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `vr_system_number` | `character varying(255)` | YES |  |  |
| `vo_system_number` | `character varying(255)` | YES |  |  |
| `vr_title` | `character varying(500)` | YES |  |  |
| `sub_con_migration_id` | `bigint(64,0)` | YES |  | FK → `public.sub_con_migration.id` |
| `vr_date` | `timestamp with time zone` | YES |  |  |
| `approval_route_id` | `integer(32,0)` | YES |  |  |
| `tax_code` | `character varying(255)` | YES |  |  |
| `tax_percentage` | `double precision` | YES | 0 |  |
| `confirm_date` | `timestamp with time zone` | YES |  |  |
| `upload_guid` | `character varying(255)` | YES |  |  |
| `upload_file_name` | `character varying(255)` | YES |  |  |
| `preview_claim_amt` | `double precision` | YES | 0 |  |
| `preview_response_amt` | `double precision` | YES | 0 |  |
| `preview_total_amt` | `double precision` | YES | 0 |  |
| `include_for_retention_cap` | `boolean` | YES | false |  |
| `variation_retention_amt` | `double precision` | YES | 0 |  |
| `vr_uuid` | `character varying(255)` | YES |  |  |
| `vo_uuid` | `character varying(255)` | YES |  |  |
| `variation_reference_number` | `character varying(255)` | YES |  |  |

**Indexes:**
- `migration_main_con_variation_id_uindex`: `CREATE UNIQUE INDEX migration_main_con_variation_id_uindex ON public.migration_main_con_variation USING btree (id)`
- `migration_main_con_variation_pk`: `CREATE UNIQUE INDEX migration_main_con_variation_pk ON public.migration_main_con_variation USING btree (id)`

#### `public.migration_main_con_variation_items`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('migration_main_con_variation... | PK |
| `work_code` | `character varying(255)` | YES |  |  |
| `description` | `character varying(2000)` | YES |  |  |
| `uom` | `character varying(255)` | YES |  |  |
| `retention` | `boolean` | YES | false |  |
| `lump_sum` | `boolean` | YES | false |  |
| `quantity` | `double precision` | YES | 0 |  |
| `unit_price` | `double precision` | YES | 0 |  |
| `cum_claim_qty` | `double precision` | YES | 0 |  |
| `cum_claim_ratio` | `double precision` | YES | 0 |  |
| `cum_response_qty` | `double precision` | YES | 0 |  |
| `cum_response_ratio` | `double precision` | YES | 0 |  |
| `remark` | `text` | YES |  |  |
| `parent_id` | `bigint(64,0)` | YES |  | FK → `public.migration_main_con_variation_items.id` |
| `migration_main_con_variation_id` | `bigint(64,0)` | YES |  | FK → `public.migration_main_con_variation.id` |
| `have_children` | `boolean` | YES | false |  |
| `cum_claim_amt` | `double precision` | YES | 0 |  |
| `cum_response_amt` | `double precision` | YES | 0 |  |
| `group_number` | `ARRAY` | YES |  |  |
| `parent_group` | `text` | YES |  |  |
| `group_code` | `character varying(255)` | YES |  |  |

#### `public.migration_material_on_site`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('migration_material_on_site_i... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `gst_code` | `character varying(255)` | YES |  |  |
| `gst_percentage` | `double precision` | YES | 0 |  |
| `upload_guid` | `character varying(255)` | YES |  |  |
| `upload_file_name` | `character varying(255)` | YES |  |  |
| `sub_con_migration_id` | `bigint(64,0)` | YES |  | FK → `public.sub_con_migration.id` |

**Indexes:**
- `migration_material_on_site_id_uindex`: `CREATE UNIQUE INDEX migration_material_on_site_id_uindex ON public.migration_material_on_site USING btree (id)`
- `migration_sub_con_variation_pk`: `CREATE UNIQUE INDEX migration_sub_con_variation_pk ON public.migration_material_on_site USING btree (id)`

#### `public.migration_preview_certificate`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('migration_preview_certificat... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `sub_con_migration_id` | `bigint(64,0)` | YES |  | FK → `public.sub_con_migration.id` |
| `original_sub_contract_sum` | `double precision` | YES | 0 |  |
| `remeasured_sub_contract_sum` | `double precision` | YES | 0 |  |
| `vo_amt` | `double precision` | YES | 0 |  |
| `adjusted_contract_sum` | `double precision` | YES | 0 |  |
| `cumulative_claim_for_original_contract_amt` | `double precision` | YES | 0 |  |
| `cumulative_vo_amt` | `double precision` | YES | 0 |  |
| `cumulative_deposit_amt` | `double precision` | YES | 0 |  |
| `cumulative_advance_payment_amt` | `double precision` | YES | 0 |  |
| `cumulative_retention_release` | `double precision` | YES | 0 |  |
| `total_gross_claim_amt` | `double precision` | YES | 0 |  |
| `materials_on_site_amt` | `double precision` | YES | 0 |  |
| `total_amount_certified` | `double precision` | YES | 0 |  |
| `cumulative_amount_variation_order` | `double precision` | YES | 0 |  |
| `final_retention_amt` | `double precision` | YES | 0 |  |
| `advance_payment_amt` | `double precision` | YES | 0 |  |
| `deposit_amt` | `double precision` | YES | 0 |  |
| `retention_release_amt` | `double precision` | YES | 0 |  |
| `previous_cum_payment_amt` | `double precision` | YES | 0 |  |
| `certified_for_this_payment_amt` | `double precision` | YES | 0 |  |
| `retention_amt` | `double precision` | YES | 0 |  |
| `deposit_refund_amt` | `double precision` | YES | 0 |  |
| `advance_payment_to_recover_amt` | `double precision` | YES | 0 |  |
| `back_charge_amt` | `double precision` | YES | 0 |  |
| `total_balance_due_amt` | `double precision` | YES | 0 |  |
| `cum_response_material_on_site_amt` | `double precision` | YES | 0 |  |
| `cum_response_original_contract_amt` | `double precision` | YES | 0 |  |
| `adjusted_variation_sum` | `double precision` | YES | 0 |  |

**Indexes:**
- `migration_preview_certificate_id_uindex`: `CREATE UNIQUE INDEX migration_preview_certificate_id_uindex ON public.migration_preview_certificate USING btree (id)`
- `migration_preview_certificate_pk`: `CREATE UNIQUE INDEX migration_preview_certificate_pk ON public.migration_preview_certificate USING btree (id)`

#### `public.migration_preview_response`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('migration_preview_response_i... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `sub_con_migration_id` | `bigint(64,0)` | YES |  | FK → `public.sub_con_migration.id` |
| `pr_reference_number` | `character varying(255)` | YES |  |  |
| `pr_date` | `timestamp with time zone` | YES |  |  |
| `project_name` | `character varying(500)` | YES |  |  |
| `contract_title` | `character varying(500)` | YES |  |  |
| `claim_date` | `timestamp with time zone` | YES |  |  |
| `claim_start_date` | `timestamp with time zone` | YES |  |  |
| `claim_end_date` | `timestamp with time zone` | YES |  |  |
| `pc_number` | `character varying(255)` | YES |  |  |
| `pc_reference_number` | `character varying(255)` | YES |  |  |
| `payment_claim_date` | `timestamp with time zone` | YES |  |  |
| `payment_claim_amt` | `double precision` | YES | 0 |  |
| `cum_for_original_contract_works_amt` | `double precision` | YES | 0 |  |
| `materials_on_site_amt` | `double precision` | YES | 0 |  |
| `cum_variation_amt` | `double precision` | YES | 0 |  |
| `ap_loan_amt` | `double precision` | YES | 0 |  |
| `ap_work_done_amt` | `double precision` | YES | 0 |  |
| `rental_deposit_amt` | `double precision` | YES | 0 |  |
| `others_deposit_amt` | `double precision` | YES | 0 |  |
| `retention_release_pb_amt` | `double precision` | YES | 0 |  |
| `retention_release_work_done_amt` | `double precision` | YES | 0 |  |
| `sub_total_amt` | `double precision` | YES | 0 |  |
| `final_retention_amt` | `double precision` | YES | 0 |  |
| `sub_total_retention_adjustment_amt` | `double precision` | YES | 0 |  |
| `previous_cum_payments_amt` | `double precision` | YES | 0 |  |
| `total_response_amt` | `double precision` | YES | 0 |  |
| `others_retention_amt` | `double precision` | YES | 0 |  |
| `rental_deposit_refund_amt` | `double precision` | YES | 0 |  |
| `others_deposit_refund_amt` | `double precision` | YES | 0 |  |
| `ap_loan_recovery_amt` | `double precision` | YES | 0 |  |
| `ap_work_done_recovery_amt` | `double precision` | YES | 0 |  |
| `back_charge_amt` | `double precision` | YES | 0 |  |
| `total_balance_due_amt` | `double precision` | YES | 0 |  |
| `cum_for_original_contract_works_response_amt` | `double precision` | YES | 0 |  |
| `materials_on_site_response_amt` | `double precision` | YES | 0 |  |
| `cum_variation_response_amt` | `double precision` | YES | 0 |  |
| `ap_loan_response_amt` | `double precision` | YES | 0 |  |
| `ap_work_done_response_amt` | `double precision` | YES | 0 |  |
| `rental_deposit_response_amt` | `double precision` | YES | 0 |  |
| `others_deposit_response_amt` | `double precision` | YES | 0 |  |
| `retention_release_pb_response_amt` | `double precision` | YES | 0 |  |
| `retention_release_work_done_response_amt` | `double precision` | YES | 0 |  |
| `sub_total_response_amt` | `double precision` | YES | 0 |  |
| `final_retention_response_amt` | `double precision` | YES | 0 |  |
| `sub_total_retention_adjustment_response_amt` | `double precision` | YES | 0 |  |

**Indexes:**
- `migration_preview_response_id_uindex`: `CREATE UNIQUE INDEX migration_preview_response_id_uindex ON public.migration_preview_response USING btree (id)`
- `migration_preview_response_pk`: `CREATE UNIQUE INDEX migration_preview_response_pk ON public.migration_preview_response USING btree (id)`

#### `public.migration_progressive_claim`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('migration_progressive_claim_... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `sub_con_migration_id` | `bigint(64,0)` | YES |  | FK → `public.sub_con_migration.id` |
| `pc_system_number` | `character varying(255)` | YES |  |  |
| `pc_reference_number` | `character varying(255)` | YES |  |  |
| `pr_reference_number` | `character varying(255)` | YES |  |  |
| `claim_month` | `timestamp with time zone` | YES |  |  |
| `approval_route_id` | `integer(32,0)` | YES |  |  |
| `tax_code` | `character varying(255)` | YES |  |  |
| `tax_percentage` | `double precision` | YES | 0 |  |
| `enable_next_claim` | `boolean` | YES | false |  |
| `title` | `character varying(500)` | YES |  |  |
| `claim_start_date` | `timestamp with time zone` | YES |  |  |
| `claim_end_date` | `timestamp with time zone` | YES |  |  |
| `notes` | `character varying(255)` | YES |  |  |
| `is_next_retention` | `boolean` | YES | false |  |
| `pc_uuid` | `character varying(255)` | YES |  |  |
| `response_date` | `timestamp with time zone` | YES |  |  |

**Indexes:**
- `migration_progressive_claim_id_uindex`: `CREATE UNIQUE INDEX migration_progressive_claim_id_uindex ON public.migration_progressive_claim USING btree (id)`
- `migration_progressive_claim_pk`: `CREATE UNIQUE INDEX migration_progressive_claim_pk ON public.migration_progressive_claim USING btree (id)`

#### `public.migration_response_summary_ref`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('migration_response_summary_r... | PK |
| `migration_progressive_claim_id` | `bigint(64,0)` | YES |  | FK → `public.migration_progressive_claim.id` |
| `applicable_performance_bond` | `boolean` | YES | false |  |
| `submitted_performance_bond` | `boolean` | YES | false |  |
| `applicable_letter_of_acceptance` | `boolean` | YES | false |  |
| `submitted_letter_of_acceptance` | `boolean` | YES | false |  |
| `applicable_warranty` | `boolean` | YES | false |  |
| `submitted_warranty` | `boolean` | YES | false |  |

**Indexes:**
- `migration_response_summary_ref_id_uindex`: `CREATE UNIQUE INDEX migration_response_summary_ref_id_uindex ON public.migration_response_summary_ref USING btree (id)`
- `migration_response_summary_ref_pk`: `CREATE UNIQUE INDEX migration_response_summary_ref_pk ON public.migration_response_summary_ref USING btree (id)`

#### `public.migration_retention_deposit_ap_release`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('migration_retention_deposit_... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `sub_con_migration_id` | `bigint(64,0)` | YES |  | FK → `public.sub_con_migration.id` |
| `rental_tax_code` | `character varying(255)` | YES |  |  |
| `rental_tax_percentage` | `double precision` | YES | 0 |  |
| `other_tax_code` | `character varying(255)` | YES |  |  |
| `other_tax_percentage` | `double precision` | YES | 0 |  |
| `work_done_tax_code` | `character varying(255)` | YES |  |  |
| `work_done_tax_percentage` | `double precision` | YES | 0 |  |
| `pb_tax_code` | `character varying(255)` | YES |  |  |
| `pb_tax_percentage` | `double precision` | YES | 0 |  |
| `loan_tax_code` | `character varying(255)` | YES |  |  |
| `loan_tax_percentage` | `double precision` | YES | 0 |  |
| `feature_tax_code` | `character varying(255)` | YES |  |  |
| `feature_tax_percentage` | `double precision` | YES | 0 |  |
| `upload_guid` | `character varying(255)` | YES |  |  |
| `upload_file_name` | `character varying(500)` | YES |  |  |

**Indexes:**
- `migration_retention_deposit_ap_release_id_uindex`: `CREATE UNIQUE INDEX migration_retention_deposit_ap_release_id_uindex ON public.migration_retention_deposit_ap_release USING btree (id)`
- `migration_retention_deposit_ap_release_pk`: `CREATE UNIQUE INDEX migration_retention_deposit_ap_release_pk ON public.migration_retention_deposit_ap_release USING btree (id)`

#### `public.migration_sub_con_variation`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('migration_sub_con_variation_... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `gst_code` | `character varying(255)` | YES |  |  |
| `gst_percentage` | `double precision` | YES | 0 |  |
| `upload_guid` | `character varying(255)` | YES |  |  |
| `upload_file_name` | `character varying(255)` | YES |  |  |
| `sub_con_migration_id` | `integer(32,0)` | YES |  | FK → `public.sub_con_migration.id` |

**Indexes:**
- `migration_sub_cmigration_sub_con_variation_tax_id_fkon_variatio`: `CREATE UNIQUE INDEX migration_sub_cmigration_sub_con_variation_tax_id_fkon_variatio ON public.migration_sub_con_variation USING btree (id)`
- `migration_sub_con_variation_id_uindex`: `CREATE UNIQUE INDEX migration_sub_con_variation_id_uindex ON public.migration_sub_con_variation USING btree (id)`

#### `public.migration_variation_items`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('migration_variation_items_id... | PK |
| `description` | `character varying(2000)` | YES |  |  |
| `sub_con_migration_id` | `bigint(64,0)` | YES |  | FK → `public.sub_con_migration.id` |
| `parent_id` | `bigint(64,0)` | YES |  | FK → `public.migration_work_contract_items.id` |
| `uom` | `character varying(255)` | YES |  |  |
| `claim_qty` | `double precision` | YES | 0 |  |
| `remarks` | `text` | YES |  |  |
| `work_code` | `character varying(255)` | YES |  |  |
| `group_code` | `character varying(255)` | YES |  |  |
| `claim_unit_price` | `double precision` | YES | 0 |  |
| `cum_claim_amt` | `double precision` | YES | 0 |  |
| `payment_response_qty` | `double precision` | YES | 0 |  |
| `cum_response_amt` | `double precision` | YES | 0 |  |
| `have_children` | `boolean` | YES | false |  |
| `payment_response_unit_price` | `double precision` | YES | 0 |  |
| `group_number` | `ARRAY` | YES |  |  |

**Indexes:**
- `migration_variation_items_id_uindex`: `CREATE UNIQUE INDEX migration_variation_items_id_uindex ON public.migration_variation_items USING btree (id)`
- `migration_variation_items_pk`: `CREATE UNIQUE INDEX migration_variation_items_pk ON public.migration_variation_items USING btree (id)`

#### `public.migration_work_contract_items`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('migration_work_contract_item... | PK |
| `description` | `character varying(2000)` | YES |  |  |
| `sub_con_migration_id` | `bigint(64,0)` | YES |  | FK → `public.sub_con_migration.id` |
| `parent_id` | `bigint(64,0)` | YES |  | FK → `public.migration_work_contract_items.id` |
| `uom` | `character varying(255)` | YES |  |  |
| `unit_price` | `double precision` | YES | 0 |  |
| `remarks` | `text` | YES |  |  |
| `work_code` | `character varying(255)` | YES |  |  |
| `group_code` | `character varying(255)` | YES |  |  |
| `quantity` | `double precision` | YES | 0 |  |
| `amount` | `double precision` | YES | 0 |  |
| `cum_claim_qty` | `double precision` | YES | 0 |  |
| `cum_claim_ratio` | `double precision` | YES | 0 |  |
| `cum_claim_amt` | `double precision` | YES | 0 |  |
| `cum_response_qty` | `double precision` | YES | 0 |  |
| `cum_response_ratio` | `double precision` | YES | 0 |  |
| `cum_response_amt` | `double precision` | YES | 0 |  |
| `have_children` | `boolean` | YES | false |  |
| `group_number` | `ARRAY` | YES |  |  |

**Indexes:**
- `migration_work_contract_items_id_uindex`: `CREATE UNIQUE INDEX migration_work_contract_items_id_uindex ON public.migration_work_contract_items USING btree (id)`
- `migration_work_contract_items_pk`: `CREATE UNIQUE INDEX migration_work_contract_items_pk ON public.migration_work_contract_items USING btree (id)`

#### `public.migration_work_order`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('migration_work_order_id_seq'... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `contract_title` | `character varying(500)` | YES |  |  |
| `contract_type` | `character varying(255)` | YES | 'LUMP_SUM'::character varying |  |
| `wr_system_number` | `character varying(255)` | YES |  |  |
| `wo_system_number` | `character varying(255)` | YES |  |  |
| `contingency` | `double precision` | YES | 0 |  |
| `retention` | `double precision` | YES | 0 |  |
| `retention_cap_at` | `double precision` | YES | 0 |  |
| `material_retention` | `double precision` | YES | 0 |  |
| `confirm_date` | `timestamp with time zone` | YES |  |  |
| `start_date` | `timestamp with time zone` | YES |  |  |
| `end_date` | `timestamp with time zone` | YES |  |  |
| `approval_route_id` | `integer(32,0)` | YES |  |  |
| `upload_guid` | `character varying(255)` | YES |  |  |
| `upload_file_name` | `character varying(255)` | YES |  |  |
| `sub_con_migration_id` | `bigint(64,0)` | YES |  | FK → `public.sub_con_migration.id` |
| `currency_id` | `bigint(64,0)` | YES |  | FK → `public.currency.id` |
| `wr_reference_number` | `character varying(255)` | YES |  |  |
| `allow_multiple_claims_in_same_month` | `boolean` | YES | false |  |
| `wr_uuid` | `character varying(255)` | YES |  |  |
| `wo_uuid` | `character varying(255)` | YES |  |  |
| `enable_deposit_and_ap_recovery` | `boolean` | YES | false |  |

**Indexes:**
- `migration_work_order_id_uindex`: `CREATE UNIQUE INDEX migration_work_order_id_uindex ON public.migration_work_order USING btree (id)`
- `migration_work_order_pk`: `CREATE UNIQUE INDEX migration_work_order_pk ON public.migration_work_order USING btree (id)`

#### `public.payment_term`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('payment_term_id_seq'::regclass) | PK |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `day` | `integer(32,0)` | NO |  |  |

#### `public.pc_audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('pc_audit_trail_id_seq'::regc... | PK |
| `progressive_claim_id` | `integer(32,0)` | YES |  | FK → `public.progressive_claim.id` |
| `user_name` | `character varying(255)` | NO |  |  |
| `user_uuid` | `character varying(255)` | NO |  |  |
| `designation` | `character varying(255)` | YES |  |  |
| `action` | `character varying(255)` | NO |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `date_time` | `timestamp with time zone` | NO |  |  |
| `remark` | `text` | YES |  |  |

#### `public.pc_back_charge_deduction_refund`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('pc_back_charge_deduction_ref... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `progressive_claim_id` | `bigint(64,0)` | YES |  | FK → `public.progressive_claim.id` |
| `back_charge_id` | `bigint(64,0)` | YES |  | FK → `public.back_charge.id` |
| `initial_pc_uuid` | `character varying(255)` | YES |  |  |
| `pc_system_number` | `character varying(500)` | YES |  |  |
| `cumulative_release` | `double precision` | YES | 0 |  |
| `balance` | `double precision` | YES | 0 |  |
| `date` | `timestamp with time zone` | YES |  |  |
| `bc_uuid` | `character varying(255)` | YES |  |  |
| `claim_month` | `timestamp with time zone` | YES |  |  |

#### `public.pc_back_charge_release_history`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('pc_back_charge_release_histo... | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `progressive_claim_id` | `bigint(64,0)` | YES |  | FK → `public.progressive_claim.id` |
| `bc_deduction_refund_id` | `bigint(64,0)` | YES |  | FK → `public.pc_back_charge_deduction_refund.id` |
| `reference_number` | `character varying(100)` | NO |  |  |
| `sub_type` | `character varying(50)` | YES |  |  |
| `description` | `character varying(500)` | YES |  |  |
| `release_amt` | `double precision` | YES | 0 |  |
| `release_date` | `timestamp with time zone` | YES |  |  |
| `created_at` | `timestamp with time zone` | YES |  |  |
| `updated_at` | `timestamp with time zone` | YES |  |  |
| `initial_pc_uuid` | `character varying(255)` | YES |  |  |
| `bc_uuid` | `character varying(255)` | YES |  |  |
| `initial_pc_number` | `character varying(255)` | YES |  |  |
| `claim_month` | `timestamp with time zone` | YES |  |  |
| `gst_available` | `boolean` | YES | false |  |
| `applicable_to_payment` | `boolean` | YES | false |  |
| `tax_rate` | `double precision` | YES | 0 |  |
| `tax_code` | `character varying(100)` | YES |  |  |
| `tax_uuid` | `character varying` | YES |  |  |

#### `public.pc_back_charge_selection`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('pc_back_charge_selection_id_... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `bc_system_number` | `character varying(255)` | YES |  |  |
| `bc_title` | `character varying(500)` | YES |  |  |
| `progressive_claim_id` | `bigint(64,0)` | YES |  | FK → `public.progressive_claim.id` |
| `back_charge_id` | `bigint(64,0)` | YES |  | FK → `public.back_charge.id` |
| `applied_pc_uuid` | `character varying(255)` | YES |  |  |
| `bc_uuid` | `character varying(255)` | YES |  |  |

#### `public.pc_deposit_ap_release`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('pc_deposit_ap_release_id_seq... | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `progressive_claim_id` | `integer(32,0)` | YES |  | FK → `public.progressive_claim.id` |
| `reference_number` | `character varying(255)` | NO |  |  |
| `description` | `character varying(2000)` | YES |  |  |
| `type` | `character varying(100)` | YES |  |  |
| `sub_type` | `character varying(200)` | YES |  |  |
| `claim_amt` | `double precision` | YES | 0 |  |
| `attachment_guid` | `character varying(100)` | YES |  |  |
| `attachment_label` | `character varying(255)` | YES |  |  |
| `response_amt` | `double precision` | YES | 0 |  |
| `cum_release_amt` | `double precision` | YES | 0 |  |
| `balance` | `double precision` | YES | 0 |  |
| `reasons_for_difference` | `character varying(500)` | YES |  |  |
| `claim_date` | `timestamp with time zone` | YES |  |  |
| `created_at` | `timestamp with time zone` | NO |  |  |
| `updated_at` | `timestamp with time zone` | YES |  |  |
| `initial_pc_number` | `character varying(255)` | YES |  |  |
| `initial_pc_uuid` | `character varying(255)` | YES |  |  |
| `claim_start_date` | `timestamp with time zone` | YES |  |  |
| `bc_uuid` | `character varying(255)` | YES |  |  |
| `cum_claim_release_amt` | `double precision` | YES | 0 |  |
| `claim_balance` | `double precision` | YES | 0 |  |
| `gst_available` | `boolean` | YES | false |  |
| `tax_rate` | `double precision` | YES | 0 |  |
| `tax_code` | `character varying(100)` | YES |  |  |
| `tax_uuid` | `character varying` | YES |  |  |
| `applicable_to_payment` | `boolean` | YES | false |  |

#### `public.pc_document`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('pc_document_id_seq'::regclass) | PK |
| `guid` | `character varying(255)` | NO |  |  |
| `label` | `character varying(255)` | NO |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `description` | `character varying(255)` | NO |  |  |
| `uploaded_by` | `character varying(255)` | NO |  |  |
| `uploader_uuid` | `character varying(255)` | NO |  |  |
| `uploaded_on` | `character varying(255)` | NO |  |  |
| `external` | `boolean` | YES | false |  |
| `progressive_claim_id` | `bigint(64,0)` | NO |  | FK → `public.progressive_claim.id` |

#### `public.pc_item`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('pc_item_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `progressive_claim_id` | `integer(32,0)` | YES |  | FK → `public.progressive_claim.id` |
| `item_group` | `character varying(100)` | NO |  |  |
| `work_code` | `character varying(255)` | NO |  |  |
| `description` | `character varying(2000)` | YES |  |  |
| `uom` | `character varying(25)` | YES |  |  |
| `retention` | `boolean` | YES | false |  |
| `lump_sum` | `boolean` | YES | false |  |
| `weightage` | `double precision` | YES | 0 |  |
| `quantity` | `double precision` | YES | 0 |  |
| `unit_price` | `double precision` | YES | 0 |  |
| `total_amount` | `double precision` | YES | 0 |  |
| `remark` | `text` | YES |  |  |
| `created_at` | `timestamp with time zone` | YES |  |  |
| `parent_id` | `integer(32,0)` | YES |  | FK → `public.pc_item.id` |
| `wo_item_id` | `integer(32,0)` | YES |  | FK → `public.work_order_item.id` |
| `wo_item_uuid` | `character varying(255)` | YES |  |  |
| `pre_cum_response_amt` | `double precision` | YES | 0 |  |
| `pre_cum_response_qty` | `double precision` | YES | 0 |  |
| `pre_cum_response_ratio` | `double precision` | YES | 0 |  |
| `cum_claim_amt` | `double precision` | YES | 0 |  |
| `cum_claim_qty` | `double precision` | YES | 0 |  |
| `cum_claim_ratio` | `double precision` | YES | 0 |  |
| `claim_amt` | `double precision` | YES | 0 |  |
| `claim_qty` | `double precision` | YES | 0 |  |
| `claim_ratio` | `double precision` | YES | 0 |  |
| `response_amt` | `double precision` | YES | 0 |  |
| `response_qty` | `double precision` | YES | 0 |  |
| `response_ratio` | `double precision` | YES | 0 |  |
| `cum_response_amt` | `double precision` | YES | 0 |  |
| `cum_response_qty` | `double precision` | YES | 0 |  |
| `cum_response_ratio` | `double precision` | YES | 0 |  |
| `response_remark` | `text` | YES |  |  |
| `claim_remark` | `character varying(500)` | YES |  |  |
| `cum_dev_response_amt` | `double precision` | YES | 0 |  |
| `cum_dev_response_ratio` | `double precision` | YES | 0 |  |
| `cum_dev_response_qty` | `double precision` | YES | 0 |  |
| `dev_response_remark` | `text` | YES |  |  |
| `parent_uuid` | `character varying(255)` | YES |  |  |
| `have_children` | `boolean` | YES | false |  |
| `retention_cap_amt` | `double precision` | YES | 0 |  |
| `claim_retention_work_done` | `double precision` | YES | 0 |  |
| `response_retention_work_done` | `double precision` | YES | 0 |  |

#### `public.pc_main_con_variation`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('pc_main_con_variation_id_seq... | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `progressive_claim_id` | `integer(32,0)` | YES |  | FK → `public.progressive_claim.id` |
| `item_group` | `character varying(100)` | NO |  |  |
| `work_code` | `character varying(255)` | NO |  |  |
| `description` | `character varying(2000)` | YES |  |  |
| `uom` | `character varying(25)` | YES |  |  |
| `retention` | `boolean` | YES | false |  |
| `remark` | `text` | YES |  |  |
| `claim_amt` | `double precision` | YES | 0 |  |
| `claim_qty` | `double precision` | YES | 0 |  |
| `claim_unit_price` | `double precision` | YES | 0 |  |
| `response_amt` | `double precision` | YES | 0 |  |
| `response_qty` | `double precision` | YES | 0 |  |
| `response_unit_price` | `double precision` | YES | 0 |  |
| `variation_type` | `character varying(25)` | YES |  |  |
| `added_to_retention_cap` | `boolean` | YES |  |  |
| `final_response` | `boolean` | YES |  |  |
| `response_remark` | `text` | YES |  |  |
| `initial_pc_number` | `character varying(255)` | YES |  |  |
| `initial_pc_uuid` | `character varying(255)` | YES |  |  |
| `parent_id` | `integer(32,0)` | YES |  | FK → `public.pc_main_con_variation.id` |
| `variation_order_id` | `integer(32,0)` | YES |  | FK → `public.variation_order.id` |
| `lump_sum` | `boolean` | YES | false |  |
| `quantity` | `double precision` | YES | 0 |  |
| `unit_price` | `double precision` | YES | 0 |  |
| `total_amount` | `double precision` | YES | 0 |  |
| `weightage` | `double precision` | YES | 0 |  |
| `pre_cum_response_amt` | `double precision` | YES | 0 |  |
| `pre_cum_response_ratio` | `double precision` | YES | 0 |  |
| `pre_cum_response_qty` | `double precision` | YES | 0 |  |
| `cum_claim_amt` | `double precision` | YES | 0 |  |
| `cum_claim_qty` | `double precision` | YES | 0 |  |
| `cum_claim_ratio` | `double precision` | YES | 0 |  |
| `claim_ratio` | `double precision` | YES | 0 |  |
| `claim_remark` | `text` | YES |  |  |
| `response_ratio` | `double precision` | YES | 0 |  |
| `cum_response_amt` | `double precision` | YES | 0 |  |
| `cum_response_qty` | `double precision` | YES | 0 |  |
| `cum_response_ratio` | `double precision` | YES | 0 |  |
| `parent_uuid` | `character varying(255)` | YES |  |  |
| `have_children` | `boolean` | YES | false |  |
| `adjusted_amt` | `double precision` | YES | 0 |  |
| `retention_cap_amt` | `double precision` | YES | 0 |  |
| `claim_retention_work_done` | `double precision` | YES | 0 |  |
| `response_retention_work_done` | `double precision` | YES | 0 |  |

#### `public.pc_material_on_site`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('pc_material_on_site_id_seq':... | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `progressive_claim_id` | `integer(32,0)` | YES |  | FK → `public.progressive_claim.id` |
| `item_group` | `character varying(100)` | NO |  |  |
| `description` | `character varying(2000)` | YES |  |  |
| `uom` | `character varying(25)` | YES |  |  |
| `do_date` | `timestamp with time zone` | YES |  |  |
| `do_number` | `character varying(100)` | YES |  |  |
| `attachment_guid` | `character varying(100)` | YES |  |  |
| `attachment_label` | `character varying(255)` | YES |  |  |
| `retention` | `boolean` | YES | false |  |
| `remark` | `text` | YES |  |  |
| `claim_amt` | `double precision` | YES | 0 |  |
| `claim_qty` | `double precision` | YES | 0 |  |
| `claim_unit_price` | `double precision` | YES | 0 |  |
| `response_amt` | `double precision` | YES | 0 |  |
| `response_qty` | `double precision` | YES | 0 |  |
| `response_unit_price` | `double precision` | YES | 0 |  |
| `response_remark` | `character varying(500)` | YES |  |  |
| `parent_id` | `integer(32,0)` | YES |  | FK → `public.pc_material_on_site.id` |
| `initial_pc_number` | `character varying(255)` | YES |  |  |
| `initial_pc_uuid` | `character varying(255)` | YES |  |  |
| `claim_start_date` | `timestamp with time zone` | YES |  |  |
| `parent_uuid` | `character varying(255)` | YES |  |  |
| `have_children` | `boolean` | YES | false |  |
| `claim_retention` | `numeric` | YES | 0 |  |
| `response_retention` | `numeric` | YES | 0 |  |
| `release_amt` | `double precision` | YES | 0 |  |
| `response_release_amt` | `double precision` | YES | 0 |  |
| `retention_release_amt` | `double precision` | YES | 0 |  |
| `response_retention_release_amt` | `double precision` | YES | 0 |  |
| `uom_uuid` | `character varying` | YES |  |  |

#### `public.pc_material_on_site_release`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('pc_material_on_site_release_... | PK |
| `pc_material_on_site_id` | `integer(32,0)` | YES |  | FK → `public.pc_material_on_site.id` |
| `release_date` | `timestamp with time zone` | YES |  |  |
| `description` | `character varying(2000)` | YES |  |  |
| `attachment_guid` | `character varying(100)` | YES |  |  |
| `attachment_label` | `character varying(255)` | YES |  |  |
| `certified_qty` | `double precision` | YES | 0 |  |
| `certified_unit_price` | `double precision` | YES | 0 |  |
| `installed_qty` | `double precision` | YES | 0 |  |
| `release_amt` | `double precision` | YES | 0 |  |
| `cum_release_amt` | `double precision` | YES | 0 |  |
| `balance` | `double precision` | YES | 0 |  |
| `response_installed_qty` | `double precision` | YES | 0 |  |
| `response_release_amt` | `double precision` | YES | 0 |  |
| `response_cum_release_amt` | `double precision` | YES | 0 |  |
| `response_balance` | `double precision` | YES | 0 |  |
| `initial_pc_number` | `character varying(255)` | YES |  |  |
| `initial_pc_uuid` | `character varying(255)` | YES |  |  |
| `claim_start_date` | `timestamp with time zone` | YES |  |  |

#### `public.pc_release_history`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('pc_release_history_id_seq'::... | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `progressive_claim_id` | `integer(32,0)` | YES |  | FK → `public.progressive_claim.id` |
| `pc_deposit_ap_release_id` | `integer(32,0)` | YES |  | FK → `public.pc_deposit_ap_release.id` |
| `reference_number` | `character varying(100)` | NO |  |  |
| `description` | `character varying(2000)` | YES |  |  |
| `release_amt` | `double precision` | YES | 0 |  |
| `release_date` | `timestamp with time zone` | YES |  |  |
| `created_at` | `timestamp with time zone` | NO |  |  |
| `updated_at` | `timestamp with time zone` | YES |  |  |
| `initial_pc_number` | `character varying(255)` | YES |  |  |
| `initial_pc_uuid` | `character varying(255)` | YES |  |  |
| `claim_start_date` | `timestamp with time zone` | YES |  |  |
| `claim_release_amt` | `double precision` | YES | 0 |  |
| `requester_name` | `character varying(255)` | YES |  |  |
| `requester_uuid` | `character varying(255)` | YES |  |  |
| `created_by_supplier` | `boolean` | YES | false |  |

#### `public.pc_response`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('pc_response_id_seq'::regclass) | PK |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `pr_reference_number` | `character varying(255)` | YES |  |  |
| `response_date` | `timestamp with time zone` | YES |  |  |
| `cum_response_original_contract_amt` | `double precision` | NO | 0 |  |
| `response_materials_amt` | `double precision` | YES | 0 |  |
| `cum_response_variation_amt` | `double precision` | NO | 0 |  |
| `advance_payment_loan` | `double precision` | YES | 0 |  |
| `advance_payment_work_done` | `double precision` | YES | 0 |  |
| `deposit_rental` | `double precision` | YES | 0 |  |
| `deposit_others` | `double precision` | YES | 0 |  |
| `retention_release_pb` | `double precision` | YES | 0 |  |
| `retention_release_work_done` | `double precision` | YES | 0 |  |
| `subtotal_before_retention_adj` | `double precision` | NO | 0 |  |
| `subtotal_after_retention_adj` | `double precision` | NO | 0 |  |
| `final_retention` | `double precision` | YES | 0 |  |
| `pre_cum_payments` | `double precision` | NO | 0 |  |
| `subtotal_response_amt` | `double precision` | NO | 0 |  |
| `retention_others` | `double precision` | YES | 0 |  |
| `advance_payment_recovery_loan` | `double precision` | YES | 0 |  |
| `advance_payment_recovery_work_done` | `double precision` | YES | 0 |  |
| `deposit_refundable_rental` | `double precision` | YES | 0 |  |
| `deposit_refundable_others` | `double precision` | YES | 0 |  |
| `back_charge_amt` | `double precision` | YES | 0 |  |
| `balance_due` | `double precision` | NO | 0 |  |
| `approval_route_id` | `integer(32,0)` | YES |  | FK → `public.approval_matrix.id` |
| `created_by_id` | `integer(32,0)` | NO |  | FK → `public.person.id` |
| `created_at` | `timestamp with time zone` | NO |  |  |
| `updated_at` | `timestamp with time zone` | YES |  |  |
| `retention_work_done` | `double precision` | YES | 0 |  |
| `retention_cap` | `double precision` | YES | 0 |  |
| `retention_materials` | `double precision` | YES | 0 |  |
| `subtotal_response_amt_with_tax` | `double precision` | YES | 0 |  |
| `balance_due_with_tax` | `double precision` | YES | 0 |  |
| `tax_amt` | `double precision` | YES | 0 |  |
| `retention_added_to_cap_subcon_vr` | `double precision` | YES | 0 |  |
| `back_charge_tax_amount` | `double precision` | YES | 0 |  |
| `back_charge_refund` | `double precision` | YES | 0 |  |
| `back_charge_deduction` | `double precision` | YES | 0 |  |
| `gst_for_bc_deduction` | `double precision` | YES | 0 |  |
| `gst_for_bc_refund` | `double precision` | YES | 0 |  |
| `notes` | `character varying(255)` | YES |  |  |
| `enable_input_retention` | `boolean` | YES | false |  |
| `tax_inv_amt` | `double precision` | YES | 0 |  |
| `applicable_to_payment_retention` | `double precision` | YES | 0 |  |
| `applicable_to_payment_bc_refund` | `double precision` | YES | 0 |  |
| `applicable_to_payment_bc_deduction` | `double precision` | YES | 0 |  |
| `applicable_to_payment_retention_release_pb` | `double precision` | YES | 0 |  |

#### `public.pc_response_reasons`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('pc_response_reasons_id_seq':... | PK |
| `description` | `character varying(100)` | NO |  |  |
| `reason_type` | `character varying(100)` | NO |  |  |
| `reason` | `character varying(500)` | YES |  |  |
| `pc_response_id` | `bigint(64,0)` | NO |  | FK → `public.pc_response.id` |
| `reasons` | `ARRAY` | YES |  |  |

#### `public.pc_response_summary_ref`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('pc_response_summary_ref_id_s... | PK |
| `reference_name` | `character varying(500)` | YES |  |  |
| `applicable` | `boolean` | YES | false |  |
| `submitted` | `boolean` | YES | false |  |
| `progressive_claim_id` | `bigint(64,0)` | YES |  | FK → `public.progressive_claim.id` |

**Indexes:**
- `pc_response_summary_ref_pk`: `CREATE UNIQUE INDEX pc_response_summary_ref_pk ON public.pc_response_summary_ref USING btree (id)`

#### `public.pc_response_tax`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('pc_response_tax_id_seq'::reg... | PK |
| `description` | `character varying(100)` | NO |  |  |
| `gst_available` | `boolean` | YES | false |  |
| `tax_code` | `character varying(100)` | YES |  |  |
| `tax_rate` | `double precision` | YES | 0 |  |
| `pc_response_id` | `bigint(64,0)` | NO |  | FK → `public.pc_response.id` |
| `tax_amt` | `double precision` | YES | 0 |  |
| `tax_uuid` | `character varying` | YES |  |  |

#### `public.pc_retention`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('pc_retention_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `progressive_claim_id` | `integer(32,0)` | YES |  | FK → `public.progressive_claim.id` |
| `reference_number` | `character varying(100)` | NO |  |  |
| `description` | `character varying(2000)` | YES |  |  |
| `amount` | `double precision` | YES | 0 |  |
| `retention_date` | `timestamp with time zone` | YES |  |  |
| `created_at` | `timestamp with time zone` | NO |  |  |
| `updated_at` | `timestamp with time zone` | YES |  |  |
| `initial_pc_number` | `character varying(255)` | YES |  |  |
| `initial_pc_uuid` | `character varying(255)` | YES |  |  |
| `claim_start_date` | `timestamp with time zone` | YES |  |  |
| `gst_available` | `boolean` | YES | false |  |
| `tax_rate` | `double precision` | YES | 0 |  |
| `tax_code` | `character varying(100)` | YES |  |  |
| `tax_uuid` | `character varying` | YES |  |  |
| `applicable_to_payment` | `boolean` | YES | false |  |

#### `public.pc_variation`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('pc_variation_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `progressive_claim_id` | `integer(32,0)` | YES |  | FK → `public.progressive_claim.id` |
| `item_group` | `character varying(100)` | NO |  |  |
| `work_code` | `character varying(255)` | NO |  |  |
| `description` | `character varying(2000)` | YES |  |  |
| `uom` | `character varying(25)` | YES |  |  |
| `retention` | `boolean` | YES | false |  |
| `remark` | `text` | YES |  |  |
| `claim_amt` | `double precision` | YES | 0 |  |
| `claim_qty` | `double precision` | YES | 0 |  |
| `claim_unit_price` | `double precision` | YES | 0 |  |
| `response_amt` | `double precision` | YES | 0 |  |
| `response_qty` | `double precision` | YES | 0 |  |
| `response_unit_price` | `double precision` | YES | 0 |  |
| `variation_type` | `character varying(100)` | YES |  |  |
| `added_to_retention_cap` | `boolean` | YES |  |  |
| `final_response` | `boolean` | YES |  |  |
| `response_remark` | `character varying(500)` | YES |  |  |
| `parent_id` | `integer(32,0)` | YES |  | FK → `public.pc_variation.id` |
| `initial_pc_number` | `character varying(255)` | YES |  |  |
| `initial_pc_uuid` | `character varying(255)` | YES |  |  |
| `parent_uuid` | `character varying(255)` | YES |  |  |
| `have_children` | `boolean` | YES | false |  |
| `claim_retention` | `numeric` | YES | 0 |  |
| `response_retention` | `numeric` | YES | 0 |  |
| `claim_retention_cap` | `numeric` | YES | 0 |  |
| `response_retention_cap` | `numeric` | YES | 0 |  |
| `final_response_retention` | `numeric` | YES | 0 |  |
| `final_response_retention_cap` | `numeric` | YES | 0 |  |
| `uom_uuid` | `character varying` | YES |  |  |

#### `public.pc_variation_workspace`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('pc_variation_workspace_id_se... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `item_group` | `character varying(255)` | YES |  |  |
| `work_code` | `character varying(255)` | YES |  |  |
| `description` | `text` | YES |  |  |
| `claim_anticipated_amount` | `double precision` | YES | 0 |  |
| `pc_variation_id` | `bigint(64,0)` | YES |  |  |
| `cumulative_claim_amount` | `double precision` | YES | 0 |  |
| `cumulative_claim_ratio` | `double precision` | YES | 0 |  |
| `claim_amount` | `double precision` | YES | 0 |  |
| `claim_remark` | `text` | YES |  |  |
| `pc_main_con_variation_id` | `bigint(64,0)` | YES |  |  |
| `previous_cumulative_response_amount` | `double precision` | YES | 0 |  |
| `cumulative_response_amount` | `double precision` | YES | 0 |  |
| `cumulative_response_ratio` | `double precision` | YES | 0 |  |
| `response_amount` | `double precision` | YES | 0 |  |
| `response_remark` | `text` | YES |  |  |
| `retention` | `boolean` | YES | false |  |
| `added_to_retention_cap` | `boolean` | YES | false |  |
| `claim_retention` | `double precision` | YES | 0 |  |
| `claim_retention_cap` | `double precision` | YES | 0 |  |
| `response_retention` | `double precision` | YES | 0 |  |
| `response_retention_cap` | `double precision` | YES | 0 |  |
| `variation_type` | `character varying(255)` | YES |  |  |
| `parent_uuid` | `character varying(255)` | YES |  |  |
| `have_children` | `boolean` | YES | false |  |
| `parent_id` | `bigint(64,0)` | YES |  | FK → `public.pc_variation_workspace.id` |
| `progressive_claim_id` | `bigint(64,0)` | YES |  | FK → `public.progressive_claim.id` |
| `response_anticipated_amount` | `double precision` | YES | 0 |  |
| `initial_pc_uuid` | `character varying(255)` | YES |  |  |
| `anticipated_amount` | `double precision` | YES | 0 |  |

#### `public.person`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('person_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `designation` | `character varying(255)` | YES |  |  |
| `email` | `character varying(255)` | NO |  |  |
| `phone_number` | `character varying(15)` | NO |  |  |
| `country_code` | `character varying(5)` | NO |  |  |
| `md5_checksum` | `character varying(255)` | NO |  |  |

#### `public.progressive_claim`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('progressive_claim_id_seq'::r... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `work_order_id` | `bigint(64,0)` | NO |  | FK → `public.work_order.id` |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `number` | `character varying(255)` | NO |  |  |
| `pc_reference_number` | `character varying(255)` | YES |  |  |
| `title` | `character varying(500)` | YES |  |  |
| `claim_start_date` | `timestamp with time zone` | NO |  |  |
| `claim_end_date` | `timestamp with time zone` | NO |  |  |
| `claim_date` | `timestamp with time zone` | NO |  |  |
| `response_date` | `timestamp with time zone` | YES |  |  |
| `status` | `character varying(100)` | NO |  |  |
| `latest_pc` | `boolean` | YES | false |  |
| `cum_claim_original_contract_amt` | `double precision` | NO | 0 |  |
| `claim_materials_amt` | `double precision` | YES | 0 |  |
| `cum_claim_variation_amt` | `double precision` | NO | 0 |  |
| `advance_payment_loan` | `double precision` | YES | 0 |  |
| `advance_payment_work_done` | `double precision` | YES | 0 |  |
| `deposit_rental` | `double precision` | YES | 0 |  |
| `deposit_others` | `double precision` | YES | 0 |  |
| `retention_release_pb` | `double precision` | YES | 0 |  |
| `retention_release_work_done` | `double precision` | YES | 0 |  |
| `subtotal_before_retention_adj` | `double precision` | NO | 0 |  |
| `retention_work_done` | `double precision` | YES | 0 |  |
| `retention_cap` | `double precision` | YES | 0 |  |
| `retention_materials` | `double precision` | YES | 0 |  |
| `final_retention` | `double precision` | YES | 0 |  |
| `pre_cum_payments` | `double precision` | NO | 0 |  |
| `claim_balance` | `double precision` | NO | 0 |  |
| `approval_route_id` | `integer(32,0)` | YES |  | FK → `public.approval_matrix.id` |
| `project_id` | `integer(32,0)` | YES |  | FK → `public.project.id` |
| `project_trade` | `character varying(255)` | YES |  |  |
| `created_by_id` | `integer(32,0)` | NO |  | FK → `public.person.id` |
| `vendor_id` | `bigint(64,0)` | YES |  | FK → `public.vendor.id` |
| `buyer_id` | `bigint(64,0)` | YES |  | FK → `public.buyer.id` |
| `created_at` | `timestamp with time zone` | NO |  |  |
| `updated_at` | `timestamp with time zone` | YES |  |  |
| `pc_response_id` | `bigint(64,0)` | YES |  | FK → `public.pc_response.id` |
| `is_developer_response` | `boolean` | YES | false |  |
| `invoice_status` | `character varying(50)` | YES |  |  |
| `retention_added_to_cap_subcon_vr` | `double precision` | YES | 0 |  |
| `is_able_ap_deposit` | `boolean` | YES | false |  |
| `claim_month` | `timestamp with time zone` | YES |  |  |
| `total_claim_amt_with_retention` | `numeric` | YES | 0 |  |
| `original_response_amt_with_retention` | `numeric` | YES | 0 |  |
| `adjusted_contract_sum` | `double precision` | YES | 0 |  |
| `adjusted_variation_sum` | `double precision` | YES | 0 |  |
| `is_next_retention` | `boolean` | YES | false |  |
| `respondent` | `bigint(64,0)` | YES |  | FK → `public.person.id` |
| `enable_input_retention` | `boolean` | YES | false |  |
| `pre_adv_payment_loan` | `double precision` | YES | 0 |  |
| `pre_adv_payment_work_done` | `double precision` | YES | 0 |  |
| `pre_deposit_rental` | `double precision` | YES | 0 |  |
| `pre_deposit_others` | `double precision` | YES | 0 |  |
| `pre_retention_release_pb` | `double precision` | YES | 0 |  |
| `pre_retention_release_work_done` | `double precision` | YES | 0 |  |
| `pre_back_charge` | `double precision` | YES | 0 |  |
| `pre_adv_payment_loan_release` | `double precision` | YES | 0 |  |
| `pre_adv_payment_work_done_release` | `double precision` | YES | 0 |  |
| `pre_deposit_rental_release` | `double precision` | YES | 0 |  |
| `pre_deposit_others_release` | `double precision` | YES | 0 |  |
| `pre_retention_release_pb_release` | `double precision` | YES | 0 |  |
| `pre_retention_release_work_done_release` | `double precision` | YES | 0 |  |
| `pre_back_charge_deduction` | `double precision` | YES | 0 |  |
| `pre_back_charge_refund` | `double precision` | YES | 0 |  |
| `pre_retention_others` | `double precision` | YES | 0 |  |
| `gst_for_pre_bc_deduction` | `double precision` | YES | 0 |  |
| `gst_for_pre_bc_refund` | `double precision` | YES | 0 |  |
| `forecast_trade_uuid` | `character varying(255)` | YES |  |  |
| `forecast_trade_label` | `character varying(255)` | YES |  |  |
| `is_able_ap_deposit_current_claim` | `boolean` | YES | false |  |
| `is_current_retention` | `boolean` | YES | false |  |
| `advance_payment_recovery_loan` | `double precision` | YES | 0 |  |
| `advance_payment_recovery_work_done` | `double precision` | YES | 0 |  |
| `deposit_refundable_rental` | `double precision` | YES | 0 |  |
| `deposit_refundable_others` | `double precision` | YES | 0 |  |
| `pre_total_amount_after_retention` | `double precision` | YES | 0 |  |
| `pre_retention_release_pb_applicable_to_payment` | `numeric(19,2)` | YES |  |  |
| `pre_back_charge_deduction_applicable_to_payment` | `numeric(19,2)` | YES |  |  |
| `pre_back_charge_refund_applicable_to_payment` | `numeric(19,2)` | YES |  |  |
| `pre_back_charge_applicable_to_payment` | `numeric(19,2)` | YES |  |  |

**Indexes:**
- `progressive_claim_company_uuid_index`: `CREATE INDEX progressive_claim_company_uuid_index ON public.progressive_claim USING btree (company_uuid)`
- `progressive_claim_status_index`: `CREATE INDEX progressive_claim_status_index ON public.progressive_claim USING btree (status)`
- `progressive_claim_uuid_index`: `CREATE INDEX progressive_claim_uuid_index ON public.progressive_claim USING btree (uuid)`

#### `public.project`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('project_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `code` | `character varying(255)` | NO |  |  |
| `title` | `character varying(500)` | NO |  |  |
| `currency` | `character varying(256)` | YES |  |  |
| `description` | `character varying(1000)` | YES |  |  |
| `md5_checksum` | `character varying(255)` | YES |  |  |

#### `public.sequence_generator`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('sequence_generator_id_seq'::... | PK |
| `company_uuid` | `character varying(50)` | YES |  |  |
| `type` | `character varying(50)` | NO |  |  |
| `number` | `character varying(50)` | NO |  |  |

**Indexes:**
- `uq_company_uuid_type`: `CREATE UNIQUE INDEX uq_company_uuid_type ON public.sequence_generator USING btree (company_uuid, type)`

#### `public.sub_con_migration`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('sub_con_migration_id_seq'::r... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `migration_number` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `status` | `character varying(100)` | YES |  |  |
| `migrated_at` | `timestamp with time zone` | YES |  |  |
| `created_by_id` | `integer(32,0)` | YES |  | FK → `public.person.id` |
| `updated_by_id` | `integer(32,0)` | YES |  | FK → `public.person.id` |
| `use_work_order` | `boolean` | YES | true |  |
| `use_progress_claim` | `boolean` | YES | false |  |
| `use_main_con_variation` | `boolean` | YES | false |  |
| `use_materials` | `boolean` | YES | false |  |
| `use_retention` | `boolean` | YES | false |  |
| `use_sub_con_variation` | `boolean` | YES | false |  |
| `use_back_charge` | `boolean` | YES | false |  |
| `created_at` | `timestamp with time zone` | YES |  |  |
| `updated_at` | `timestamp with time zone` | YES |  |  |
| `migrated_by_id` | `integer(32,0)` | YES |  | FK → `public.person.id` |
| `vendor_id` | `bigint(64,0)` | YES |  | FK → `public.vendor.id` |
| `project_id` | `bigint(64,0)` | YES |  | FK → `public.project.id` |
| `project_trade` | `character varying(255)` | YES |  |  |
| `nature_project` | `boolean` | YES | false |  |
| `bc_system_number` | `text` | YES |  |  |
| `vo_system_number` | `text` | YES |  |  |
| `respondent` | `bigint(64,0)` | YES |  | FK → `public.person.id` |
| `reason` | `text` | YES |  |  |
| `forecast_trade_uuid` | `character varying(255)` | YES |  |  |
| `forecast_trade_label` | `character varying(255)` | YES |  |  |

**Indexes:**
- `sub_con_migration_company_uuid_uindex`: `CREATE INDEX sub_con_migration_company_uuid_uindex ON public.sub_con_migration USING btree (company_uuid)`
- `sub_con_migration_id_uindex`: `CREATE UNIQUE INDEX sub_con_migration_id_uindex ON public.sub_con_migration USING btree (id)`
- `sub_con_migration_pk`: `CREATE UNIQUE INDEX sub_con_migration_pk ON public.sub_con_migration USING btree (id)`
- `sub_con_migration_status_uindex`: `CREATE INDEX sub_con_migration_status_uindex ON public.sub_con_migration USING btree (status)`

#### `public.tax`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('tax_id_seq'::regclass) | PK |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `rate` | `double precision` | NO |  |  |

#### `public.variation_order`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('variation_order_id_seq'::reg... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `number` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `variation_request_id` | `bigint(64,0)` | YES |  | FK → `public.variation_request.id` |
| `title` | `character varying(255)` | YES |  |  |
| `total_amount` | `double precision` | NO | 0 |  |
| `work_order_id` | `bigint(64,0)` | YES |  | FK → `public.work_order.id` |
| `approval_route_id` | `bigint(64,0)` | YES |  | FK → `public.approval_matrix.id` |
| `buyer_id` | `bigint(64,0)` | YES |  | FK → `public.buyer.id` |
| `vendor_id` | `bigint(64,0)` | YES |  | FK → `public.vendor.id` |
| `created_by_id` | `bigint(64,0)` | NO |  | FK → `public.person.id` |
| `created_at` | `timestamp with time zone` | NO |  |  |
| `updated_at` | `timestamp with time zone` | YES |  |  |
| `claim_total` | `double precision` | YES | 0 |  |
| `response_total` | `double precision` | YES | 0 |  |
| `claim_retention` | `double precision` | YES | 0 |  |
| `response_retention` | `double precision` | YES | 0 |  |
| `include_for_retention_cap` | `boolean` | YES | false |  |
| `variation_retention_amt` | `double precision` | YES | 0 |  |

#### `public.variation_order_audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('variation_order_audit_trail_... | PK |
| `action` | `character varying(255)` | YES |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `date_time` | `timestamp with time zone` | NO |  |  |
| `designation` | `character varying(255)` | YES |  |  |
| `remark` | `text` | YES |  |  |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `variation_order_id` | `bigint(64,0)` | YES |  | FK → `public.variation_order.id` |

#### `public.variation_order_document`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('variation_order_document_id_... | PK |
| `description` | `character varying(500)` | YES |  |  |
| `external` | `boolean` | YES | false |  |
| `guid` | `character varying(255)` | YES |  |  |
| `label` | `character varying(255)` | YES |  |  |
| `name` | `character varying(255)` | YES |  |  |
| `uploaded_by` | `character varying(255)` | YES |  |  |
| `uploaded_on` | `character varying(255)` | YES |  |  |
| `uploader_uuid` | `character varying(255)` | YES |  |  |
| `variation_order_id` | `bigint(64,0)` | YES |  | FK → `public.variation_order.id` |

#### `public.variation_order_item`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('variation_order_item_id_seq'... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `item_group` | `character varying(255)` | YES |  |  |
| `work_code` | `character varying(255)` | YES |  |  |
| `description` | `character varying(2000)` | YES |  |  |
| `uom` | `character varying(255)` | YES |  |  |
| `retention` | `boolean` | YES | false |  |
| `lump_sum` | `boolean` | YES | false |  |
| `quantity` | `double precision` | YES | 0 |  |
| `unit_price` | `double precision` | YES | 0 |  |
| `total_amount` | `double precision` | YES | 0 |  |
| `weightage` | `double precision` | YES | 0 |  |
| `remark` | `text` | YES |  |  |
| `parent_id` | `bigint(64,0)` | YES |  | FK → `public.variation_order_item.id` |
| `variation_order_id` | `bigint(64,0)` | YES |  | FK → `public.variation_order.id` |
| `pre_cum_response_amt` | `double precision` | YES | 0 |  |
| `pre_cum_response_qty` | `double precision` | YES | 0 |  |
| `pre_cum_response_ratio` | `double precision` | YES | 0 |  |
| `cum_claim_amt` | `double precision` | YES | 0 |  |
| `cum_claim_qty` | `double precision` | YES | 0 |  |
| `cum_claim_ratio` | `double precision` | YES | 0 |  |
| `claim_amt` | `double precision` | YES | 0 |  |
| `claim_qty` | `double precision` | YES | 0 |  |
| `claim_ratio` | `double precision` | YES | 0 |  |
| `claim_remark` | `text` | YES |  |  |
| `response_amt` | `double precision` | YES | 0 |  |
| `response_qty` | `double precision` | YES | 0 |  |
| `response_ratio` | `double precision` | YES | 0 |  |
| `cum_response_amt` | `double precision` | YES | 0 |  |
| `cum_response_qty` | `double precision` | YES | 0 |  |
| `cum_response_ratio` | `double precision` | YES | 0 |  |
| `response_remark` | `text` | YES |  |  |
| `parent_uuid` | `character varying(255)` | YES |  |  |
| `have_children` | `boolean` | YES | false |  |
| `adjusted_amt` | `double precision` | YES | 0 |  |
| `retention_cap_amt` | `double precision` | YES | 0 |  |
| `claim_retention_work_done` | `double precision` | YES | 0 |  |
| `response_retention_work_done` | `double precision` | YES | 0 |  |
| `uom_uuid` | `character varying` | YES |  |  |

#### `public.variation_request`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('variation_request_id_seq'::r... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `created_at` | `timestamp with time zone` | NO |  |  |
| `number` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `title` | `character varying(255)` | YES |  |  |
| `total_amount` | `double precision` | NO | 0 |  |
| `updated_at` | `timestamp with time zone` | NO |  |  |
| `variation_date` | `timestamp with time zone` | YES |  |  |
| `variation_reference_number` | `character varying(255)` | YES |  |  |
| `approval_route_id` | `bigint(64,0)` | YES |  | FK → `public.approval_matrix.id` |
| `buyer_id` | `bigint(64,0)` | YES |  | FK → `public.buyer.id` |
| `vendor_id` | `bigint(64,0)` | YES |  | FK → `public.vendor.id` |
| `work_order_id` | `bigint(64,0)` | YES |  | FK → `public.work_order.id` |
| `created_by_id` | `bigint(64,0)` | YES |  | FK → `public.person.id` |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `include_for_retention_cap` | `boolean` | YES | false |  |
| `variation_retention_amt` | `double precision` | YES | 0 |  |

#### `public.variation_request_audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('variation_request_audit_trai... | PK |
| `action` | `character varying(255)` | YES |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `date_time` | `timestamp with time zone` | NO |  |  |
| `designation` | `character varying(255)` | YES |  |  |
| `remark` | `text` | YES |  |  |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `variation_request_id` | `bigint(64,0)` | YES |  | FK → `public.variation_request.id` |

#### `public.variation_request_document`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('variation_request_document_i... | PK |
| `description` | `character varying(500)` | YES |  |  |
| `external` | `boolean` | YES | false |  |
| `guid` | `character varying(255)` | YES |  |  |
| `label` | `character varying(255)` | YES |  |  |
| `name` | `character varying(255)` | YES |  |  |
| `uploaded_by` | `character varying(255)` | YES |  |  |
| `uploaded_on` | `character varying(255)` | YES |  |  |
| `uploader_uuid` | `character varying(255)` | YES |  |  |
| `variation_request_id` | `bigint(64,0)` | YES |  | FK → `public.variation_request.id` |

#### `public.variation_request_item`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('variation_request_item_id_se... | PK |
| `description` | `character varying(2000)` | YES |  |  |
| `item_group` | `character varying(255)` | YES |  |  |
| `lump_sum` | `boolean` | YES | false |  |
| `quantity` | `double precision` | YES | 0 |  |
| `remark` | `text` | YES |  |  |
| `retention` | `boolean` | YES | false |  |
| `total_amount` | `double precision` | YES | 0 |  |
| `unit_price` | `double precision` | YES | 0 |  |
| `uom` | `character varying(255)` | YES |  |  |
| `uuid` | `character varying(255)` | YES |  |  |
| `weightage` | `double precision` | YES | 0 |  |
| `work_code` | `character varying(255)` | YES |  |  |
| `parent_id` | `bigint(64,0)` | YES |  | FK → `public.variation_request_item.id` |
| `variation_request_id` | `bigint(64,0)` | YES |  | FK → `public.variation_request.id` |
| `migrated_claim_qty` | `double precision` | YES | 0 |  |
| `migrated_claim_percentage` | `double precision` | YES | 0 |  |
| `migrated_response_qty` | `double precision` | YES | 0 |  |
| `migrated_response_percentage` | `double precision` | YES | 0 |  |
| `migrated_cum_claim_qty` | `double precision` | YES | 0 |  |
| `migrated_cum_claim_percentage` | `double precision` | YES | 0 |  |
| `migrated_cum_response_qty` | `double precision` | YES | 0 |  |
| `migrated_cum_response_percentage` | `double precision` | YES | 0 |  |
| `parent_uuid` | `character varying(255)` | YES |  |  |
| `have_children` | `boolean` | YES | false |  |
| `uom_uuid` | `character varying` | YES |  |  |
| `migrated_claim_remark` | `character varying(500)` | YES |  |  |
| `migrated_response_remark` | `character varying(500)` | YES |  |  |

#### `public.vendor`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('vendor_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `code` | `character varying(50)` | NO |  |  |
| `country` | `character varying(50)` | NO |  |  |
| `gst_no` | `character varying(50)` | YES |  |  |
| `company_reg_no` | `character varying(50)` | YES |  |  |
| `uen` | `character varying(50)` | NO |  |  |
| `md5_checksum` | `character varying(255)` | NO |  |  |
| `person_id` | `bigint(64,0)` | YES |  | FK → `public.person.id` |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `address_id` | `bigint(64,0)` | YES |  | FK → `public.address.id` |

#### `public.work_order`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('work_order_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `number` | `character varying(255)` | NO |  |  |
| `status` | `character varying(100)` | NO |  |  |
| `work_request_id` | `bigint(64,0)` | NO |  | FK → `public.work_request.id` |
| `title` | `character varying(500)` | YES |  |  |
| `contract_type` | `character varying(255)` | NO | 'LUMP_SUM'::character varying |  |
| `project_id` | `integer(32,0)` | YES |  | FK → `public.project.id` |
| `project_trade` | `character varying(255)` | YES |  |  |
| `adjusted_contract_sum` | `double precision` | YES | 0 |  |
| `contract_start_date` | `timestamp with time zone` | YES |  |  |
| `confirmation_date` | `timestamp with time zone` | YES |  |  |
| `contract_duration` | `integer(32,0)` | NO | 0 |  |
| `setting_id` | `integer(32,0)` | NO |  | FK → `public.wr_setting.id` |
| `original_contract_sum` | `double precision` | NO | 0 |  |
| `contingency_sum` | `double precision` | NO | 0 |  |
| `variation_sum` | `double precision` | NO | 0 |  |
| `remeasured_contract_sum` | `double precision` | YES | 0 |  |
| `retention` | `double precision` | YES | 0 |  |
| `retention_capped_at` | `double precision` | YES |  |  |
| `retention_amount_capped_at` | `double precision` | YES | 0 |  |
| `created_by_id` | `integer(32,0)` | NO |  | FK → `public.person.id` |
| `created_at` | `timestamp with time zone` | NO |  |  |
| `vendor_id` | `bigint(64,0)` | YES |  | FK → `public.vendor.id` |
| `updated_at` | `timestamp with time zone` | YES |  |  |
| `currency_id` | `bigint(64,0)` | YES |  | FK → `public.currency.id` |
| `is_project` | `boolean` | NO | false |  |
| `buyer_id` | `bigint(64,0)` | YES |  | FK → `public.buyer.id` |
| `material_retention` | `double precision` | YES | 0 |  |
| `cum_response_amt` | `double precision` | YES | 0 |  |
| `contract_end_date` | `timestamp with time zone` | YES |  |  |
| `allow_multiple_claims_in_same_month` | `boolean` | YES | false |  |
| `latest_pc_number` | `character varying(255)` | YES |  |  |
| `latest_pc_uuid` | `character varying(255)` | YES |  |  |
| `latest_pc_month` | `timestamp without time zone` | YES |  |  |
| `respondent` | `bigint(64,0)` | YES |  | FK → `public.person.id` |
| `forecast_trade_uuid` | `character varying(255)` | YES |  |  |
| `forecast_trade_label` | `character varying(255)` | YES |  |  |
| `buyer_latest_pc_number` | `character varying(255)` | YES |  |  |
| `buyer_latest_pc_uuid` | `character varying(255)` | YES |  |  |
| `buyer_latest_pc_month` | `timestamp without time zone` | YES |  |  |
| `level` | `double precision` | YES | 0 |  |
| `parent_work_order_id` | `bigint(64,0)` | YES |  | FK → `public.work_order.id` |
| `root_work_order_id` | `bigint(64,0)` | YES |  | FK → `public.work_order.id` |
| `tagged_item_id` | `integer(32,0)` | YES |  | FK → `public.work_order_item.id` |

**Indexes:**
- `work_order_company_uuid_index`: `CREATE INDEX work_order_company_uuid_index ON public.work_order USING btree (company_uuid)`
- `work_order_status_index`: `CREATE INDEX work_order_status_index ON public.work_order USING btree (status)`
- `work_order_uuid_index`: `CREATE INDEX work_order_uuid_index ON public.work_order USING btree (uuid)`

#### `public.work_order_audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('work_order_audit_trail_id_se... | PK |
| `work_order_id` | `integer(32,0)` | YES |  | FK → `public.work_order.id` |
| `user_name` | `character varying(255)` | NO |  |  |
| `user_uuid` | `character varying(255)` | NO |  |  |
| `designation` | `character varying(255)` | YES |  |  |
| `action` | `character varying(50)` | NO |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `date_time` | `timestamp with time zone` | NO |  |  |
| `remark` | `text` | YES |  |  |

#### `public.work_order_document`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('work_order_document_id_seq':... | PK |
| `guid` | `character varying(255)` | NO |  |  |
| `label` | `character varying(255)` | NO |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `description` | `character varying(255)` | NO |  |  |
| `uploaded_by` | `character varying(255)` | NO |  |  |
| `uploader_uuid` | `character varying(255)` | NO |  |  |
| `uploaded_on` | `character varying(255)` | NO |  |  |
| `external` | `boolean` | YES | false |  |
| `work_order_id` | `bigint(64,0)` | NO |  | FK → `public.work_order.id` |

#### `public.work_order_item`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('work_order_item_id_seq'::reg... | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `work_order_id` | `integer(32,0)` | YES |  | FK → `public.work_order.id` |
| `item_group` | `character varying(100)` | NO |  |  |
| `work_code` | `character varying(255)` | NO |  |  |
| `description` | `character varying(2000)` | YES |  |  |
| `uom` | `character varying(25)` | YES |  |  |
| `retention` | `boolean` | YES | false |  |
| `lump_sum` | `boolean` | YES | false |  |
| `weightage` | `double precision` | YES | 0 |  |
| `quantity` | `double precision` | YES | 0 |  |
| `unit_price` | `double precision` | YES | 0 |  |
| `total_amount` | `double precision` | YES | 0 |  |
| `remark` | `text` | YES |  |  |
| `parent_id` | `integer(32,0)` | YES |  | FK → `public.work_order_item.id` |
| `pre_cum_response_amt` | `double precision` | YES | 0 |  |
| `pre_cum_response_qty` | `double precision` | YES | 0 |  |
| `pre_cum_response_ratio` | `double precision` | YES | 0 |  |
| `cum_claim_amt` | `double precision` | YES | 0 |  |
| `cum_claim_qty` | `double precision` | YES | 0 |  |
| `cum_claim_ratio` | `double precision` | YES | 0 |  |
| `cum_response_amt` | `double precision` | YES | 0 |  |
| `cum_response_qty` | `double precision` | YES | 0 |  |
| `cum_response_ratio` | `double precision` | YES | 0 |  |
| `response_remark` | `text` | YES |  |  |
| `parent_uuid` | `character varying(255)` | YES |  |  |
| `have_children` | `boolean` | YES | false |  |
| `retention_cap_amt` | `double precision` | YES | 0 |  |
| `claim_retention_work_done` | `double precision` | YES | 0 |  |
| `response_retention_work_done` | `double precision` | YES | 0 |  |
| `uom_uuid` | `character varying(36)` | YES |  |  |
| `tagged_item_id` | `integer(32,0)` | YES |  | FK → `public.work_order_item.id` |

#### `public.work_request`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('work_request_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `number` | `character varying(255)` | NO |  |  |
| `status` | `character varying(100)` | NO |  |  |
| `work_reference_number` | `character varying(255)` | YES |  |  |
| `title` | `character varying(500)` | YES |  |  |
| `approval_route_id` | `integer(32,0)` | YES |  |  |
| `contract_type` | `character varying(255)` | NO | 'LUMP_SUM'::character varying |  |
| `project_id` | `integer(32,0)` | YES |  | FK → `public.project.id` |
| `project_trade` | `character varying(255)` | YES |  |  |
| `adjusted_contract_sum` | `double precision` | YES | 0 |  |
| `contract_start_date` | `timestamp with time zone` | YES |  |  |
| `contract_duration` | `integer(32,0)` | NO | 0 |  |
| `setting_id` | `integer(32,0)` | NO |  | FK → `public.wr_setting.id` |
| `original_contract_sum` | `double precision` | NO | 0 |  |
| `contingency_sum` | `double precision` | NO | 0 |  |
| `variation_sum` | `double precision` | NO | 0 |  |
| `remeasured_contract_sum` | `double precision` | YES | 0 |  |
| `retention` | `double precision` | YES | 0 |  |
| `retention_capped_at` | `double precision` | YES |  |  |
| `retention_amount_capped_at` | `double precision` | YES | 0 |  |
| `created_by_id` | `integer(32,0)` | NO |  | FK → `public.person.id` |
| `created_at` | `timestamp with time zone` | NO |  |  |
| `vendor_id` | `bigint(64,0)` | YES |  | FK → `public.vendor.id` |
| `updated_at` | `timestamp with time zone` | YES |  |  |
| `currency_id` | `bigint(64,0)` | YES |  | FK → `public.currency.id` |
| `is_project` | `boolean` | NO | false |  |
| `buyer_id` | `bigint(64,0)` | YES |  | FK → `public.buyer.id` |
| `material_retention` | `double precision` | YES | 0 |  |
| `vendor_viewed` | `boolean` | NO | false |  |
| `contract_end_date` | `timestamp with time zone` | YES |  |  |
| `allow_multiple_claims_in_same_month` | `boolean` | YES | false |  |
| `respondent` | `bigint(64,0)` | YES |  | FK → `public.person.id` |
| `forecast_trade_uuid` | `character varying(255)` | YES |  |  |
| `forecast_trade_label` | `character varying(255)` | YES |  |  |
| `level` | `double precision` | YES | 0 |  |
| `root_work_request_id` | `bigint(64,0)` | YES |  | FK → `public.work_request.id` |
| `parent_work_request_id` | `bigint(64,0)` | YES |  | FK → `public.work_request.id` |
| `tagged_item_id` | `integer(32,0)` | YES |  | FK → `public.work_order_item.id` |

**Indexes:**
- `work_request_company_uuid_index`: `CREATE INDEX work_request_company_uuid_index ON public.work_request USING btree (company_uuid)`
- `work_request_status_index`: `CREATE INDEX work_request_status_index ON public.work_request USING btree (status)`
- `work_request_uuid_index`: `CREATE INDEX work_request_uuid_index ON public.work_request USING btree (uuid)`

#### `public.work_request_item`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('work_request_item_id_seq'::r... | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `work_request_id` | `integer(32,0)` | YES |  | FK → `public.work_request.id` |
| `item_group` | `character varying(100)` | NO |  |  |
| `work_code` | `character varying(255)` | NO |  |  |
| `description` | `character varying(2000)` | YES |  |  |
| `uom` | `character varying(25)` | YES |  |  |
| `retention` | `boolean` | YES | false |  |
| `lump_sum` | `boolean` | YES | false |  |
| `weightage` | `double precision` | YES | 0 |  |
| `quantity` | `double precision` | YES | 0 |  |
| `unit_price` | `double precision` | YES | 0 |  |
| `total_amount` | `double precision` | YES | 0 |  |
| `remark` | `text` | YES |  |  |
| `created_at` | `timestamp with time zone` | YES |  |  |
| `parent_id` | `integer(32,0)` | YES |  | FK → `public.work_request_item.id` |
| `parent_uuid` | `character varying(255)` | YES |  |  |
| `have_children` | `boolean` | YES | false |  |
| `uom_uuid` | `character varying(36)` | YES |  |  |
| `tagged_item_id` | `integer(32,0)` | YES |  | FK → `public.work_request_item.id` |

#### `public.wr_audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('wr_audit_trail_id_seq'::regc... | PK |
| `work_request_id` | `integer(32,0)` | YES |  | FK → `public.work_request.id` |
| `user_name` | `character varying(255)` | NO |  |  |
| `user_uuid` | `character varying(255)` | NO |  |  |
| `designation` | `character varying(255)` | YES |  |  |
| `action` | `character varying(50)` | NO |  |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `date_time` | `timestamp with time zone` | NO |  |  |
| `remark` | `text` | YES |  |  |

#### `public.wr_document`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('wr_document_id_seq'::regclass) | PK |
| `guid` | `character varying(255)` | NO |  |  |
| `label` | `character varying(255)` | NO |  |  |
| `name` | `character varying(255)` | NO |  |  |
| `description` | `character varying(255)` | NO |  |  |
| `uploaded_by` | `character varying(255)` | NO |  |  |
| `uploader_uuid` | `character varying(255)` | NO |  |  |
| `uploaded_on` | `character varying(255)` | NO |  |  |
| `external` | `boolean` | YES | false |  |
| `work_request_id` | `bigint(64,0)` | NO |  | FK → `public.work_request.id` |

#### `public.wr_setting`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO | nextval('wr_setting_id_seq'::regclass) | PK |
| `enable_deposit_and_ap_recovery` | `boolean` | YES | false |  |
| `enable_contingency_sum` | `boolean` | YES | false |  |

---

## purchase

**Schemas:** public
**Total tables:** 52

### Schema: `public`

#### `public.addresses`

- **Type:** BASE TABLE  **Rows:** 1705

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('addresses_id_seq'::regclass) | PK |
| `address_label` | `character varying(100)` | NO |  |  |
| `address_first_line` | `character varying(500)` | NO |  |  |
| `address_second_line` | `character varying(200)` | YES |  |  |
| `city` | `character varying(100)` | YES |  |  |
| `state` | `character varying(100)` | NO |  |  |
| `country` | `character varying(100)` | NO |  |  |
| `postal_code` | `character varying(20)` | NO |  |  |
| `md5check_sum` | `character varying(255)` | YES |  |  |
| `uuid` | `character varying(255)` | YES |  |  |

#### `public.buyer_information`

- **Type:** BASE TABLE  **Rows:** 1128

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('buyer_information_id_seq'::r... | PK |
| `buyer_code` | `character varying(50)` | NO |  |  |
| `buyer_name` | `character varying(150)` | NO |  |  |
| `country` | `character varying(50)` | NO |  |  |
| `company_reg_no` | `character varying(150)` | NO |  |  |
| `uuid` | `character varying(255)` | YES |  |  |
| `gst_no` | `character varying(50)` | YES |  |  |
| `uen` | `character varying(50)` | YES |  |  |
| `md5check_sum` | `character varying(500)` | YES |  |  |
| `contact_person_id` | `bigint(64,0)` | YES |  |  |
| `address_id` | `bigint(64,0)` | YES |  |  |

#### `public.contact_person`

- **Type:** BASE TABLE  **Rows:** 3891

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('contact_person_id_seq'::regc... | PK |
| `name` | `character varying(255)` | YES |  |  |
| `phone_number` | `character varying(255)` | YES |  |  |
| `country_code` | `character varying(50)` | YES |  |  |
| `email` | `character varying(500)` | YES |  |  |
| `md5check_sum` | `character varying(255)` | YES |  |  |
| `uuid` | `character varying(255)` | YES |  |  |

**Indexes:**
- `contact_person_id_uindex`: `CREATE UNIQUE INDEX contact_person_id_uindex ON public.contact_person USING btree (id)`
- `contact_person_pk`: `CREATE UNIQUE INDEX contact_person_pk ON public.contact_person USING btree (id)`

#### `public.delivery_instruction`

- **Type:** BASE TABLE  **Rows:** 248

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('delivery_instruction_id_seq'... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `di_number` | `character varying(255)` | YES |  |  |
| `di_global_number` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `delivery_date` | `timestamp without time zone` | YES |  |  |
| `created_date` | `timestamp without time zone` | YES | now() |  |
| `issued_date` | `timestamp without time zone` | YES |  |  |
| `po_number` | `character varying(255)` | YES |  |  |
| `do_uuid_list` | `text` | YES |  |  |
| `po_uuid` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `procurement_type` | `character varying(255)` | YES |  |  |
| `buyer_id` | `bigint(64,0)` | YES |  | FK → `public.buyer_information.id` |
| `buyer_contact_person_id` | `bigint(64,0)` | YES |  | FK → `public.contact_person.id` |
| `supplier_contact_person_id` | `bigint(64,0)` | YES |  | FK → `public.contact_person.id` |
| `supplier_company_uuid` | `character varying(255)` | YES |  |  |
| `supplier_id` | `bigint(64,0)` | YES |  | FK → `public.suppliers.id` |
| `currency_code` | `character varying(255)` | YES |  |  |
| `project_code` | `character varying(255)` | YES |  |  |
| `project_code_uuid` | `character varying(255)` | YES |  |  |
| `project_title` | `character varying(255)` | YES |  |  |
| `reason` | `character varying(255)` | YES |  |  |
| `created_by` | `character varying(255)` | YES |  |  |
| `approval_route_name` | `character varying(100)` | YES |  |  |
| `approval_route_sequence` | `character varying(255)` | YES |  |  |
| `approval_route_uuid` | `character varying(100)` | YES |  |  |
| `next_approver` | `character varying(255)` | YES |  |  |
| `next_approval_group_uuid` | `character varying(255)` | YES |  |  |
| `do_status` | `character varying(255)` | YES |  |  |
| `creator_uuid` | `character varying(255)` | YES |  |  |

#### `public.delivery_instruction_audit_trail`

- **Type:** BASE TABLE  **Rows:** 721

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('delivery_instruction_audit_t... | PK |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `user_name` | `character varying(255)` | YES |  |  |
| `role` | `character varying(255)` | YES |  |  |
| `action` | `character varying(255)` | YES |  |  |
| `created_date` | `timestamp without time zone` | YES | CURRENT_TIMESTAMP |  |
| `delivery_instruction_id` | `bigint(64,0)` | YES |  | FK → `public.delivery_instruction.id` |

#### `public.delivery_instruction_item`

- **Type:** BASE TABLE  **Rows:** 409

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('delivery_instruction_item_id... | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `po_number` | `character varying(255)` | YES |  |  |
| `po_uuid` | `character varying(255)` | YES |  |  |
| `cat_item_id` | `bigint(64,0)` | YES |  |  |
| `item_code` | `character varying(255)` | YES |  |  |
| `item_name` | `character varying(255)` | YES |  |  |
| `item_description` | `character varying(255)` | YES |  |  |
| `item_category` | `character varying(255)` | YES |  |  |
| `item_category_uuid` | `character varying(255)` | YES |  |  |
| `item_unit_price` | `numeric(25,2)` | YES |  |  |
| `quantity` | `numeric(25,2)` | YES |  |  |
| `po_quantity` | `numeric(25,2)` | YES |  |  |
| `item_model` | `character varying(255)` | YES |  |  |
| `item_size` | `character varying(255)` | YES |  |  |
| `item_brand` | `character varying(255)` | YES |  |  |
| `price_type` | `character varying(255)` | YES |  |  |
| `uom_code` | `character varying(255)` | YES |  |  |
| `qty_received` | `numeric(25,2)` | YES | 0 |  |
| `qty_to_convert` | `numeric(25,2)` | YES | 0 |  |
| `qty_rejected` | `numeric(25,2)` | YES | 0 |  |
| `qty_to_convert_str` | `character varying(255)` | YES | '0'::character varying |  |
| `address_id` | `bigint(64,0)` | YES |  | FK → `public.addresses.id` |
| `request_delivery_date` | `timestamp without time zone` | YES |  |  |
| `po_note` | `character varying(255)` | YES |  |  |
| `notes_to_supplier` | `character varying(255)` | YES |  |  |
| `comments_on_delivery` | `character varying(255)` | YES |  |  |
| `po_item_id` | `bigint(64,0)` | YES |  | FK → `public.po_item.id` |
| `delivery_instruction_id` | `bigint(64,0)` | YES |  | FK → `public.delivery_instruction.id` |
| `invoice_qty` | `numeric(25,2)` | YES | 0 |  |
| `invoice_rejected_qty` | `numeric(25,2)` | YES | 0 |  |
| `over_purchased_qty` | `boolean` | YES | false |  |

#### `public.delivery_order`

- **Type:** BASE TABLE  **Rows:** 3964

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('delivery_order_id_seq'::regc... | PK |
| `delivery_order_number` | `character varying(50)` | NO |  |  |
| `global_do_number` | `character varying(50)` | NO |  |  |
| `status` | `character varying(255)` | NO |  |  |
| `delivery_date` | `timestamp with time zone` | NO |  |  |
| `created_date` | `timestamp with time zone` | NO | now() |  |
| `issued_date` | `timestamp with time zone` | YES |  |  |
| `po_list` | `character varying(255)` | NO |  |  |
| `procurement_type` | `character varying(50)` | NO |  |  |
| `company_uuid` | `character varying(255)` | NO |  |  |
| `buyer_id` | `bigint(64,0)` | YES |  | FK → `public.buyer_information.id` |
| `uuid` | `character varying(255)` | NO |  |  |
| `buyer_contact_person` | `bigint(64,0)` | YES |  | FK → `public.contact_person.id` |
| `currency_code` | `character varying(50)` | YES |  |  |
| `buyer_company_uuid` | `character varying(255)` | YES |  |  |
| `supplier_id` | `bigint(64,0)` | YES |  | FK → `public.suppliers.id` |
| `project_code` | `character varying(50)` | YES |  |  |
| `project_code_uuid` | `character varying(50)` | YES |  |  |
| `project_title` | `character varying(1000)` | YES |  |  |
| `created_by` | `character varying(50)` | YES |  |  |
| `is_integration` | `boolean` | YES | false |  |
| `submitted_staff` | `character varying(50)` | YES |  |  |
| `updated_at` | `timestamp with time zone` | YES | now() |  |
| `do_type` | `character varying(10)` | YES |  |  |
| `transaction_type_uuid` | `character varying(255)` | YES |  |  |
| `transaction_type_code` | `character varying(255)` | YES |  |  |
| `transaction_type_name` | `character varying(255)` | YES |  |  |

**Indexes:**
- `delivery_order_buyer_company_uuid_index`: `CREATE INDEX delivery_order_buyer_company_uuid_index ON public.delivery_order USING btree (buyer_company_uuid)`
- `delivery_order_company_uuid_index`: `CREATE INDEX delivery_order_company_uuid_index ON public.delivery_order USING btree (company_uuid)`
- `delivery_order_uuid_index`: `CREATE INDEX delivery_order_uuid_index ON public.delivery_order USING btree (uuid)`
- `unique_company_delivery_order_number_except_manual`: `CREATE UNIQUE INDEX unique_company_delivery_order_number_except_manual ON public.delivery_order USING btree (delivery_order_number, company_uuid) WHERE ((delivery_order_number)::text IS DISTINCT FROM 'Manual'::text)`
- `uq_company_do_number`: `CREATE UNIQUE INDEX uq_company_do_number ON public.delivery_order USING btree (company_uuid, delivery_order_number)`

#### `public.delivery_order_audit_trail`

- **Type:** BASE TABLE  **Rows:** 5686

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('delivery_order_audit_trail_i... | PK |
| `user_uuid` | `character varying(50)` | NO |  |  |
| `user_name` | `character varying(100)` | NO |  |  |
| `role` | `character varying(50)` | YES |  |  |
| `action` | `character varying(255)` | NO |  |  |
| `created_date` | `timestamp with time zone` | NO | now() |  |
| `delivery_order_id` | `bigint(64,0)` | YES |  | FK → `public.delivery_order.id` |
| `remark` | `character varying(255)` | YES |  |  |

#### `public.delivery_order_document_metadata`

- **Type:** BASE TABLE  **Rows:** 143

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('delivery_order_document_meta... | PK |
| `guid` | `character varying(50)` | NO |  |  |
| `file_label` | `character varying(255)` | NO |  |  |
| `file_description` | `character varying(255)` | NO |  |  |
| `uploaded_on` | `timestamp with time zone` | NO | now() |  |
| `uploaded_by_name` | `character varying(100)` | NO |  |  |
| `uploaded_by_uuid` | `character varying(50)` | NO |  |  |
| `delivery_order_id` | `bigint(64,0)` | YES |  | FK → `public.delivery_order.id` |
| `file_name` | `character varying(255)` | YES |  |  |

#### `public.delivery_order_item`

- **Type:** BASE TABLE  **Rows:** 7001

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('delivery_order_item_id_seq':... | PK |
| `purchase_order_number` | `character varying(255)` | NO |  |  |
| `purchase_order_uuid` | `character varying(255)` | NO |  |  |
| `item_code` | `character varying(100)` | NO |  |  |
| `item_name` | `character varying(255)` | NO |  |  |
| `item_description` | `text` | YES |  |  |
| `item_model` | `character varying(255)` | YES |  |  |
| `item_size` | `character varying(500)` | YES |  |  |
| `item_brand` | `character varying(255)` | YES |  |  |
| `uom_code` | `character varying(50)` | YES |  |  |
| `po_quantity` | `numeric(25,12)` | YES | 0 |  |
| `qty_converted` | `numeric(25,12)` | YES | 0 |  |
| `qty_received` | `numeric(25,12)` | YES | 0 |  |
| `qty_to_convert` | `numeric(25,12)` | YES | 0 |  |
| `qty_rejected` | `numeric(25,12)` | YES | 0 |  |
| `address_id` | `bigint(64,0)` | YES |  | FK → `public.addresses.id` |
| `po_note` | `character varying(3000)` | YES |  |  |
| `notes_to_buyer` | `character varying(500)` | YES |  |  |
| `comments_on_delivery` | `character varying(1000)` | YES |  |  |
| `document_guid` | `character varying(255)` | YES |  |  |
| `document_file_label` | `character varying(255)` | YES |  |  |
| `gr_qty_received` | `numeric(25,12)` | YES | 0 |  |
| `gr_qty_rejected` | `numeric(25,12)` | YES | 0 |  |
| `delivery_order_id` | `bigint(64,0)` | YES |  | FK → `public.delivery_order.id` |
| `invoice_qty` | `numeric(25,12)` | YES | 0 |  |
| `invoice_rejected_qty` | `numeric(25,12)` | YES | 0 |  |
| `po_item_id` | `bigint(64,0)` | YES |  |  |
| `invoice_pending_approval_qty` | `numeric(25,12)` | YES | 0 |  |
| `price_type` | `character varying(100)` | YES |  |  |
| `contracted` | `boolean` | YES | false |  |
| `contract_reference_number` | `character varying(500)` | YES |  |  |
| `contracted_price` | `numeric(25,12)` | YES | 0 |  |
| `item_uuid` | `character varying(255)` | YES |  |  |
| `cat_item_id` | `bigint(64,0)` | YES |  |  |
| `qty_to_convert_str` | `character varying(255)` | YES | ''::character varying |  |
| `over_purchased_qty` | `boolean` | NO | false |  |
| `di_item_id` | `bigint(64,0)` | YES |  |  |

**Indexes:**
- `delivery_order_item_delivery_order_id_index`: `CREATE INDEX delivery_order_item_delivery_order_id_index ON public.delivery_order_item USING btree (delivery_order_id)`
- `delivery_order_item_po_item_id_index`: `CREATE INDEX delivery_order_item_po_item_id_index ON public.delivery_order_item USING btree (po_item_id)`

#### `public.email_template`

- **Type:** BASE TABLE  **Rows:** 73

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('email_template_id_seq'::regc... | PK |
| `feature_code` | `character varying(50)` | YES |  |  |
| `action` | `character varying(50)` | YES |  |  |
| `subject` | `character varying(500)` | YES |  |  |
| `content` | `text` | YES |  |  |

**Indexes:**
- `email_template_id_uindex`: `CREATE UNIQUE INDEX email_template_id_uindex ON public.email_template USING btree (id)`
- `email_template_pk`: `CREATE UNIQUE INDEX email_template_pk ON public.email_template USING btree (id)`

#### `public.erp_api_configuration`

- **Type:** BASE TABLE  **Rows:** 3

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `company_uuid` | `character varying(100)` | NO |  |  |
| `api_type` | `character varying(250)` | NO |  |  |
| `api_url` | `character varying(250)` | NO |  |  |
| `user_name` | `character varying(100)` | YES |  |  |
| `password` | `character varying(100)` | YES |  |  |
| `id` | `integer(32,0)` | NO | nextval('erp_api_configuration_id_seq... |  |

**Indexes:**
- `erp_api_configuration_company_api_type_idx`: `CREATE UNIQUE INDEX erp_api_configuration_company_api_type_idx ON public.erp_api_configuration USING btree (company_uuid, api_type)`

#### `public.goods_receipt`

- **Type:** BASE TABLE  **Rows:** 3597

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('goods_receipt_id_seq'::regcl... | PK |
| `company_uuid` | `character varying(50)` | YES |  |  |
| `gr_number` | `character varying(50)` | YES |  |  |
| `uuid` | `character varying(50)` | YES |  |  |
| `gr_global_number` | `character varying(50)` | YES |  |  |
| `gr_type` | `character varying(50)` | YES |  |  |
| `gr_status` | `character varying(100)` | YES |  |  |
| `delivery_order_number` | `character varying(50)` | YES |  |  |
| `delivery_date` | `timestamp with time zone` | YES |  |  |
| `receiver_uuid` | `character varying(50)` | YES |  |  |
| `receiver_name` | `character varying(255)` | YES |  |  |
| `procurement_type` | `character varying(50)` | YES |  |  |
| `approval_route_name` | `character varying(255)` | YES |  |  |
| `approval_route_sequence` | `text` | YES |  |  |
| `approval_route_uuid` | `character varying(100)` | YES |  |  |
| `next_approver` | `character varying(255)` | YES |  |  |
| `submitted_date` | `timestamp with time zone` | NO | now() |  |
| `approved_date` | `timestamp with time zone` | YES |  |  |
| `suppliers_id` | `bigint(64,0)` | YES |  | FK → `public.suppliers.id` |
| `next_approval_group_uuid` | `character varying(255)` | YES |  |  |
| `supplier_company_uuid` | `character varying(255)` | YES |  |  |
| `receipt_date` | `timestamp with time zone` | YES |  |  |
| `original_delivery_date` | `timestamp with time zone` | YES |  |  |
| `project_code` | `character varying(250)` | YES |  |  |
| `do_status` | `character varying(255)` | YES |  |  |

**Indexes:**
- `goods_receipt_companyuuid_grglobalnumber_index`: `CREATE INDEX goods_receipt_companyuuid_grglobalnumber_index ON public.goods_receipt USING btree (company_uuid, gr_global_number)`
- `goods_receipt_companyuuid_index`: `CREATE INDEX goods_receipt_companyuuid_index ON public.goods_receipt USING btree (company_uuid)`
- `goods_receipt_companyuuid_uuid_grglobalnumber_index`: `CREATE INDEX goods_receipt_companyuuid_uuid_grglobalnumber_index ON public.goods_receipt USING btree (company_uuid, uuid, gr_global_number)`
- `goods_receipt_companyuuid_uuid_index`: `CREATE INDEX goods_receipt_companyuuid_uuid_index ON public.goods_receipt USING btree (company_uuid, uuid)`
- `uq_company_gr_number`: `CREATE UNIQUE INDEX uq_company_gr_number ON public.goods_receipt USING btree (company_uuid, gr_number)`

#### `public.goods_receipt_audit_trail`

- **Type:** BASE TABLE  **Rows:** 5182

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('goods_receipt_audit_trail_id... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(50)` | YES |  |  |
| `action` | `character varying(100)` | YES |  |  |
| `date_time` | `timestamp with time zone` | NO | now() |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `goods_receipt_id` | `bigint(64,0)` | YES |  | FK → `public.goods_receipt.id` |
| `remark` | `character varying(1000)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |

**Indexes:**
- `goods_receipt_audit_trail_goodsreceiptid_index`: `CREATE INDEX goods_receipt_audit_trail_goodsreceiptid_index ON public.goods_receipt_audit_trail USING btree (goods_receipt_id)`

#### `public.goods_receipt_document_metadata`

- **Type:** BASE TABLE  **Rows:** 105

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('goods_receipt_document_metad... | PK |
| `guid` | `character varying(50)` | YES |  |  |
| `file_label` | `character varying(255)` | YES |  |  |
| `file_description` | `character varying(255)` | YES |  |  |
| `uploaded_on` | `timestamp with time zone` | NO | now() |  |
| `uploaded_by` | `character varying(100)` | YES |  |  |
| `uploader_uuid` | `character varying(50)` | YES |  |  |
| `external_document` | `boolean` | YES |  |  |
| `goods_receipt_id` | `bigint(64,0)` | YES |  | FK → `public.goods_receipt.id` |
| `file_name` | `character varying(255)` | YES |  |  |

**Indexes:**
- `goods_receipt_document_metadata_goodsreceiptid_index`: `CREATE INDEX goods_receipt_document_metadata_goodsreceiptid_index ON public.goods_receipt_document_metadata USING btree (goods_receipt_id)`

#### `public.goods_receipt_item`

- **Type:** BASE TABLE  **Rows:** 6564

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('goods_receipt_item_id_seq'::... | PK |
| `delivery_order_uuid` | `character varying(50)` | YES |  |  |
| `delivery_order_number` | `character varying(50)` | YES |  |  |
| `purchase_order_uuid` | `character varying(50)` | YES |  |  |
| `purchase_order_number` | `character varying(50)` | YES |  |  |
| `item_code` | `character varying(100)` | YES |  |  |
| `item_name` | `character varying(255)` | YES |  |  |
| `item_description` | `text` | YES |  |  |
| `item_model` | `character varying(255)` | YES |  |  |
| `item_size` | `character varying(500)` | YES |  |  |
| `item_brand` | `character varying(255)` | YES |  |  |
| `uom_code` | `character varying(50)` | YES |  |  |
| `po_quantity` | `numeric(25,12)` | NO | 0 |  |
| `qty_received` | `numeric(25,12)` | NO | 0 |  |
| `qty_rejected` | `numeric(25,12)` | NO | 0 |  |
| `qty_pending_delivery` | `numeric(25,12)` | NO | 0 |  |
| `qty_converted` | `numeric(25,12)` | NO | 0 |  |
| `delivery_order_quantity` | `numeric(25,12)` | NO | 0 |  |
| `qty_receiving` | `numeric(25,12)` | NO | 0 |  |
| `qty_rejecting` | `numeric(25,12)` | NO | 0 |  |
| `po_delivery_completed` | `boolean` | YES |  |  |
| `addresses_id` | `bigint(64,0)` | YES |  |  |
| `notes_to_buyer` | `character varying(1000)` | YES |  |  |
| `comments_on_delivery` | `character varying(1000)` | YES |  |  |
| `document_guid` | `character varying(50)` | YES |  |  |
| `document_file_label` | `character varying(255)` | YES |  |  |
| `goods_receipt_id` | `bigint(64,0)` | YES |  | FK → `public.goods_receipt.id` |
| `po_item_id` | `bigint(64,0)` | YES |  |  |
| `do_item_id` | `bigint(64,0)` | YES |  |  |
| `price_type` | `character varying(100)` | YES |  |  |
| `contracted` | `boolean` | YES | false |  |
| `contract_reference_number` | `character varying(500)` | YES |  |  |
| `contracted_price` | `numeric(25,12)` | YES | 0 |  |
| `item_uuid` | `character varying(255)` | YES |  |  |
| `cat_item_id` | `bigint(64,0)` | YES |  |  |
| `qty_receiving_str` | `character varying(255)` | YES | ''::character varying |  |
| `close_po` | `boolean` | YES | false |  |
| `over_pending_delivery_qty` | `boolean` | NO | false |  |
| `uom_uuid` | `character varying` | YES |  |  |
| `qty_do_converted` | `numeric(25,12)` | YES | 0 |  |
| `expiry_date` | `timestamp with time zone` | YES |  |  |
| `reference_number` | `character varying(50)` | YES |  |  |

**Indexes:**
- `goods_receipt_item_goodsreceiptid_index`: `CREATE INDEX goods_receipt_item_goodsreceiptid_index ON public.goods_receipt_item USING btree (goods_receipt_id)`

#### `public.liquibase-changelog`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `character varying(255)` | NO |  |  |
| `author` | `character varying(255)` | NO |  |  |
| `filename` | `character varying(255)` | NO |  |  |
| `dateexecuted` | `timestamp without time zone` | NO |  |  |
| `orderexecuted` | `integer(32,0)` | NO |  |  |
| `exectype` | `character varying(10)` | NO |  |  |
| `md5sum` | `character varying(35)` | YES |  |  |
| `description` | `character varying(255)` | YES |  |  |
| `comments` | `character varying(255)` | YES |  |  |
| `tag` | `character varying(255)` | YES |  |  |
| `liquibase` | `character varying(20)` | YES |  |  |
| `contexts` | `character varying(255)` | YES |  |  |
| `labels` | `character varying(255)` | YES |  |  |
| `deployment_id` | `character varying(10)` | YES |  |  |

#### `public.liquibase-lock`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `integer(32,0)` | NO |  | PK |
| `locked` | `boolean` | NO |  |  |
| `lockgranted` | `timestamp without time zone` | YES |  |  |
| `lockedby` | `character varying(255)` | YES |  |  |

**Indexes:**
- `LIQUIBASE-LOCK_PKEY`: `CREATE UNIQUE INDEX "LIQUIBASE-LOCK_PKEY" ON public."liquibase-lock" USING btree (id)`

#### `public.po_audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('po_audit_trail_id_seq'::regc... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `role` | `character varying(255)` | YES |  |  |
| `current_group` | `character varying(255)` | YES |  |  |
| `action` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `date` | `timestamp with time zone` | YES | now() |  |
| `po_id` | `bigint(64,0)` | YES |  | FK → `public.purchase_order.id` |
| `remark` | `character varying(1000)` | YES |  |  |

#### `public.po_document`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('po_document_id_seq'::regclass) | PK |
| `guid` | `character varying(255)` | YES |  |  |
| `title` | `character varying(255)` | YES |  |  |
| `file_name` | `character varying(255)` | YES |  |  |
| `description` | `character varying(255)` | YES |  |  |
| `upload_by` | `character varying(255)` | YES |  |  |
| `uploader_uuid` | `character varying(255)` | YES |  |  |
| `external_document` | `boolean` | YES |  |  |
| `upload_on` | `timestamp with time zone` | NO | now() |  |
| `po_id` | `bigint(64,0)` | YES |  | FK → `public.purchase_order.id` |
| `file_label` | `character varying(255)` | YES |  |  |

#### `public.po_item`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('po_item_id_seq'::regclass) | PK |
| `item_code` | `character varying(100)` | YES |  |  |
| `item_name` | `character varying(255)` | YES |  |  |
| `item_description` | `text` | YES |  |  |
| `item_model` | `character varying(255)` | YES |  |  |
| `item_size` | `character varying(500)` | YES |  |  |
| `item_brand` | `character varying(255)` | YES |  |  |
| `supplier_name` | `character varying(255)` | YES |  |  |
| `supplier_uuid` | `character varying(50)` | YES |  |  |
| `uom_code` | `character varying(50)` | YES |  |  |
| `currency` | `character varying(50)` | YES |  |  |
| `item_unit_price` | `numeric(25,12)` | YES |  |  |
| `quantity` | `numeric(25,12)` | YES | 0 |  |
| `tax_code` | `character varying(50)` | YES |  |  |
| `tax_rate` | `double precision` | YES |  |  |
| `exchange_rate` | `double precision` | YES | 0 |  |
| `delivery_address_id` | `bigint(64,0)` | NO |  | FK → `public.addresses.id` |
| `request_delivery_date` | `timestamp with time zone` | YES |  |  |
| `gl_account` | `character varying(50)` | YES |  |  |
| `note` | `character varying(3000)` | YES |  |  |
| `po_id` | `bigint(64,0)` | YES |  | FK → `public.purchase_order.id` |
| `manual_entry` | `boolean` | YES |  |  |
| `project_forecast_trade_code` | `character varying(50)` | YES |  |  |
| `quantity_received` | `numeric(25,12)` | NO | 0 |  |
| `quantity_previously_delivered` | `double precision` | YES | 0 |  |
| `quantity_pending_receipt_approval` | `numeric(25,12)` | NO | 0 |  |
| `invoice_qty` | `numeric(25,12)` | NO | 0 |  |
| `qty_converted` | `numeric(25,12)` | NO | 0 |  |
| `qty_rejected` | `numeric(25,12)` | NO | 0 |  |
| `company_uuid` | `character varying(50)` | YES |  |  |
| `invoice_rejected_qty` | `numeric(25,12)` | NO | 0 |  |
| `invoice_pending_approval_qty` | `numeric(25,12)` | YES | 0 |  |
| `original_qty` | `numeric(25,12)` | YES | 0 |  |
| `item_category_uuid` | `character varying(255)` | YES |  |  |
| `item_category` | `character varying(100)` | YES |  |  |
| `price_type` | `character varying(100)` | YES |  |  |
| `tax_amount` | `numeric(26,2)` | YES | 0 |  |
| `sub_total` | `numeric(26,2)` | YES | 0 |  |
| `net_price` | `numeric(26,2)` | YES | 0 |  |
| `contracted` | `boolean` | YES | false |  |
| `contracted_price` | `numeric(25,12)` | YES | 0 |  |
| `contract_reference_number` | `character varying(500)` | YES |  |  |
| `item_uuid` | `character varying(255)` | YES |  |  |
| `item_unit_price_str` | `character varying(255)` | YES | ''::character varying |  |
| `quantity_str` | `character varying(255)` | YES | ''::character varying |  |
| `exchange_rate_str` | `character varying(255)` | YES | ''::character varying |  |
| `cat_item_id` | `bigint(64,0)` | YES |  |  |
| `discount_amount` | `numeric(26,2)` | YES | 0 |  |
| `contracted_price_str` | `character varying(255)` | YES | NULL::character varying |  |
| `forecast_trade_uuid` | `character varying(255)` | YES |  |  |
| `forecast_trade_label` | `character varying(255)` | YES |  |  |
| `tax_uuid` | `character varying` | YES |  |  |
| `uom_uuid` | `character varying` | YES |  |  |
| `gl_description` | `character varying(255)` | YES |  |  |
| `work_done_month` | `date` | YES |  |  |

**Indexes:**
- `po_item_po_id_index`: `CREATE INDEX po_item_po_id_index ON public.po_item USING btree (po_id)`

#### `public.po_item_discount`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('po_item_discount_id_seq'::re... | PK |
| `amount` | `numeric(26,2)` | YES | 0 |  |
| `is_percent_off` | `boolean` | YES | false |  |
| `po_item_id` | `bigint(64,0)` | YES |  | FK → `public.po_item.id` |
| `amount_str` | `character varying(255)` | YES | ''::character varying |  |

#### `public.ppr_audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('ppr_audit_trail_id_seq'::reg... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `role` | `character varying(255)` | YES |  |  |
| `current_group` | `character varying(255)` | YES |  |  |
| `action` | `character varying(255)` | YES |  |  |
| `status` | `character varying(255)` | YES |  |  |
| `date` | `timestamp with time zone` | YES | now() |  |
| `ppr_id` | `bigint(64,0)` | YES |  | FK → `public.pre_purchase_requisition.id` |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `remark` | `character varying(1000)` | YES |  |  |
| `document_references` | `character varying` | YES |  |  |

**Indexes:**
- `ppr_audit_trail_index`: `CREATE INDEX ppr_audit_trail_index ON public.ppr_audit_trail USING btree (ppr_id)`

#### `public.ppr_document`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('ppr_document_id_seq'::regclass) | PK |
| `guid` | `character varying(255)` | YES |  |  |
| `title` | `character varying(255)` | YES |  |  |
| `file_name` | `character varying(255)` | YES |  |  |
| `description` | `character varying(255)` | YES |  |  |
| `upload_by` | `character varying(255)` | YES |  |  |
| `uploader_uuid` | `character varying(255)` | YES |  |  |
| `upload_on` | `timestamp with time zone` | NO | now() |  |
| `ppr_id` | `bigint(64,0)` | YES |  | FK → `public.pre_purchase_requisition.id` |
| `external_document` | `boolean` | YES |  |  |
| `file_label` | `character varying(255)` | YES |  |  |

**Indexes:**
- `ppr_document_index`: `CREATE INDEX ppr_document_index ON public.ppr_document USING btree (ppr_id)`

#### `public.ppr_items`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('ppr_items_id_seq'::regclass) | PK |
| `item_code` | `character varying(100)` | YES |  |  |
| `item_name` | `character varying(255)` | YES |  |  |
| `item_description` | `text` | YES |  |  |
| `item_model` | `character varying(255)` | YES |  |  |
| `item_size` | `character varying(500)` | YES |  |  |
| `item_brand` | `character varying(255)` | YES |  |  |
| `item_type` | `character varying(255)` | YES |  |  |
| `item_category` | `character varying(255)` | YES |  |  |
| `item_material` | `character varying(255)` | YES |  |  |
| `uom_code` | `character varying(50)` | YES |  |  |
| `quantity` | `numeric(25,12)` | NO |  |  |
| `delivery_address_id` | `bigint(64,0)` | YES |  | FK → `public.addresses.id` |
| `request_delivery_date` | `timestamp with time zone` | YES |  |  |
| `note` | `character varying(3000)` | YES |  |  |
| `ppr_id` | `bigint(64,0)` | YES |  | FK → `public.pre_purchase_requisition.id` |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `manual_entry` | `boolean` | YES |  |  |
| `item_category_uuid` | `character varying(255)` | YES |  |  |
| `contracted` | `boolean` | YES | false |  |
| `contracted_price` | `numeric(25,12)` | YES | 0 |  |
| `contract_reference_number` | `character varying(500)` | YES |  |  |
| `item_uuid` | `character varying(255)` | YES |  |  |
| `supplier_name` | `character varying(500)` | YES |  |  |
| `supplier_uuid` | `character varying(255)` | YES |  |  |
| `gl_account` | `character varying(50)` | YES |  |  |
| `source_currency` | `character varying(50)` | YES |  |  |
| `tax_code` | `character varying(50)` | YES |  |  |
| `tax_rate` | `numeric(15,2)` | YES |  |  |
| `trade_code` | `character varying(50)` | YES |  |  |
| `quantity_str` | `character varying(255)` | YES | ''::character varying |  |
| `cat_item_id` | `bigint(64,0)` | YES |  |  |
| `contracted_price_str` | `character varying(255)` | YES | NULL::character varying |  |
| `forecast_trade_uuid` | `character varying(255)` | YES |  |  |
| `forecast_trade_label` | `character varying(255)` | YES |  |  |
| `converted_quantity` | `numeric(25,12)` | YES | 0 |  |
| `fully_converted` | `boolean` | YES | false |  |
| `tax_uuid` | `character varying` | YES |  |  |
| `uom_uuid` | `character varying` | YES |  |  |

**Indexes:**
- `ppr_item_index`: `CREATE INDEX ppr_item_index ON public.ppr_items USING btree (ppr_id)`

#### `public.pre_po`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('pre_po_id_seq'::regclass) | PK |
| `company_uuid` | `character varying(50)` | YES |  |  |
| `pre_po_global_number` | `character varying(255)` | YES |  |  |
| `uuid` | `character varying(255)` | YES | uuid_generate_v4() |  |
| `pre_po_title` | `character varying(100)` | YES |  |  |
| `procurement_type` | `character varying(50)` | YES |  |  |
| `pre_po_number` | `character varying(50)` | YES |  |  |
| `pre_po_status` | `character varying(255)` | YES |  |  |
| `total_amount` | `numeric(26,2)` | YES |  |  |
| `approval_route_name` | `character varying(100)` | YES |  |  |
| `approval_route_sequence` | `character varying(255)` | YES |  |  |
| `approval_route_uuid` | `character varying(100)` | YES |  |  |
| `next_approver` | `character varying(255)` | YES |  |  |
| `purchaser_uuid` | `character varying(50)` | YES |  |  |
| `purchaser_name` | `character varying(255)` | YES |  |  |
| `payment_terms` | `character varying(255)` | YES |  |  |
| `converted_date` | `timestamp with time zone` | NO | now() |  |
| `updated_date` | `timestamp with time zone` | NO | now() |  |
| `suppliers_id` | `bigint(64,0)` | YES |  | FK → `public.suppliers.id` |
| `addresses_id` | `bigint(64,0)` | YES |  | FK → `public.addresses.id` |
| `remarks` | `text` | YES |  |  |
| `converted_to_po` | `boolean` | YES |  |  |
| `purchase_req_id` | `bigint(64,0)` | YES |  |  |
| `approved_date` | `timestamp with time zone` | YES | now() |  |
| `currency` | `character varying(20)` | YES |  |  |
| `supplier_uuid` | `character varying(255)` | YES |  |  |
| `supplier_name` | `character varying(1000)` | YES |  |  |
| `next_approval_group_uuid` | `character varying(255)` | YES |  |  |
| `project_title` | `character varying(1000)` | YES |  |  |
| `project_code` | `character varying(200)` | YES |  |  |
| `project_uuid` | `character varying(255)` | YES |  |  |
| `submitted_date` | `timestamp with time zone` | YES |  |  |
| `requester_uuid` | `character varying(255)` | YES |  |  |
| `requester_name` | `character varying(255)` | YES |  |  |
| `currency_name` | `character varying(255)` | YES |  |  |

**Indexes:**
- `prepo_companyuuid_index`: `CREATE INDEX prepo_companyuuid_index ON public.pre_po USING btree (company_uuid)`
- `prepo_companyuuid_prepoglobalnumber_index`: `CREATE INDEX prepo_companyuuid_prepoglobalnumber_index ON public.pre_po USING btree (company_uuid, pre_po_global_number)`
- `prepo_companyuuid_preponumber_index`: `CREATE INDEX prepo_companyuuid_preponumber_index ON public.pre_po USING btree (company_uuid, pre_po_number)`
- `prepo_companyuuid_prepostatus_index`: `CREATE INDEX prepo_companyuuid_prepostatus_index ON public.pre_po USING btree (company_uuid, pre_po_status)`
- `prepo_companyuuid_uuid_index`: `CREATE INDEX prepo_companyuuid_uuid_index ON public.pre_po USING btree (company_uuid, uuid)`
- `prepo_companyuuid_uuid_prepoglobalnumber_index`: `CREATE INDEX prepo_companyuuid_uuid_prepoglobalnumber_index ON public.pre_po USING btree (company_uuid, uuid, pre_po_global_number)`

#### `public.pre_po_audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('pre_po_audit_trail_id_seq'::... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(50)` | YES |  |  |
| `action` | `character varying(100)` | YES |  |  |
| `date_time` | `timestamp with time zone` | NO | now() |  |
| `approval_group` | `character varying(100)` | YES |  |  |
| `pre_po_id` | `bigint(64,0)` | YES |  | FK → `public.pre_po.id` |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `remark` | `text` | YES |  |  |

**Indexes:**
- `prepoaudittrail_prepoid_index`: `CREATE INDEX prepoaudittrail_prepoid_index ON public.pre_po_audit_trail USING btree (pre_po_id)`

#### `public.pre_po_document_metadata`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('pre_po_document_metadata_id_... | PK |
| `guid` | `character varying(50)` | YES |  |  |
| `file_label` | `character varying(255)` | YES |  |  |
| `file_description` | `character varying(255)` | YES |  |  |
| `uploaded_on` | `timestamp with time zone` | NO | now() |  |
| `uploaded_by` | `character varying(100)` | YES |  |  |
| `uploader_uuid` | `character varying(50)` | YES |  |  |
| `external_document` | `boolean` | YES |  |  |
| `pre_po_id` | `bigint(64,0)` | YES |  | FK → `public.pre_po.id` |

#### `public.pre_po_item`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('pre_po_item_id_seq'::regclass) | PK |
| `item_code` | `character varying(50)` | YES |  |  |
| `item_name` | `character varying(255)` | YES |  |  |
| `item_description` | `text` | YES |  |  |
| `item_model` | `character varying(255)` | YES |  |  |
| `item_size` | `character varying(200)` | YES |  |  |
| `item_brand` | `character varying(255)` | YES |  |  |
| `source_currency` | `character varying(50)` | YES |  |  |
| `uom_code` | `character varying(50)` | YES |  |  |
| `item_unit_price` | `numeric(25,12)` | YES |  |  |
| `item_quantity` | `numeric(25,12)` | YES |  |  |
| `tax_code` | `character varying(50)` | YES |  |  |
| `tax_rate` | `double precision` | YES |  |  |
| `exchange_rate` | `double precision` | YES |  |  |
| `addresses_id` | `bigint(64,0)` | NO |  | FK → `public.addresses.id` |
| `requested_delivery_date` | `timestamp with time zone` | NO | now() |  |
| `gl_account` | `character varying(50)` | YES |  |  |
| `note` | `character varying(3000)` | YES |  |  |
| `pre_po_id` | `bigint(64,0)` | YES |  | FK → `public.pre_po.id` |
| `manual_item` | `boolean` | YES |  |  |
| `project_forecast_trade_code` | `character varying(50)` | YES |  |  |
| `company_uuid` | `character varying(50)` | YES |  |  |
| `item_category_uuid` | `character varying(255)` | YES |  |  |
| `item_category` | `character varying(50)` | YES |  |  |
| `price_type` | `character varying(100)` | YES |  |  |

**Indexes:**
- `prepoitem_prepoid_index`: `CREATE INDEX prepoitem_prepoid_index ON public.pre_po_item USING btree (pre_po_id)`

#### `public.pre_purchase_requisition`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('pre_purchase_requisition_id_... | PK |
| `ppr_number` | `character varying(50)` | NO |  |  |
| `ppr_global_number` | `character varying(255)` | YES |  |  |
| `status` | `character varying(50)` | YES |  |  |
| `ppr_title` | `character varying(100)` | YES |  |  |
| `currency_code` | `character varying(20)` | YES |  |  |
| `procurement_type` | `character varying(20)` | YES |  |  |
| `submitted_on` | `timestamp with time zone` | YES | now() |  |
| `updated_on` | `timestamp with time zone` | YES | now() |  |
| `note` | `character varying(3000)` | YES |  |  |
| `approval_code_uuid` | `character varying(255)` | YES |  |  |
| `approval_sequence` | `text` | YES |  |  |
| `approval_code` | `character varying(255)` | YES |  |  |
| `next_group` | `character varying(255)` | YES |  |  |
| `requester_name` | `character varying(255)` | YES |  |  |
| `requester_uuid` | `character varying(255)` | YES |  |  |
| `project_code` | `character varying(50)` | YES |  |  |
| `converted_to_pr` | `boolean` | YES |  |  |
| `project` | `boolean` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `uuid` | `character varying(255)` | YES |  |  |
| `next_group_uuid` | `character varying(255)` | YES |  |  |
| `project_title` | `character varying(1000)` | YES |  |  |
| `project_uuid` | `character varying(255)` | YES |  |  |
| `currency_name` | `character varying(255)` | YES |  |  |
| `approved_date` | `timestamp with time zone` | YES |  |  |
| `addresses_id` | `bigint(64,0)` | YES |  | FK → `public.addresses.id` |
| `requested_delivery_date` | `timestamp with time zone` | YES |  |  |
| `delivery_contact_person_id` | `bigint(64,0)` | YES |  | FK → `public.contact_person.id` |
| `transaction_type_uuid` | `character varying(255)` | YES |  |  |
| `transaction_type_code` | `character varying(255)` | YES |  |  |
| `transaction_type_name` | `character varying(255)` | YES |  |  |

**Indexes:**
- `ppr_company_index`: `CREATE INDEX ppr_company_index ON public.pre_purchase_requisition USING btree (company_uuid)`
- `ppr_companyandpprnumber_index`: `CREATE INDEX ppr_companyandpprnumber_index ON public.pre_purchase_requisition USING btree (company_uuid, ppr_number)`

#### `public.price_comparison`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('price_comparison_id_seq'::re... | PK |
| `uuid` | `character varying(36)` | YES | uuid_generate_v4() |  |
| `company_uuid` | `character varying(36)` | NO |  |  |
| `cat_item_id` | `bigint(64,0)` | YES |  |  |
| `item_name` | `character varying(255)` | YES |  |  |
| `item_code` | `character varying(50)` | YES |  |  |
| `supplier_name` | `character varying(255)` | NO |  |  |
| `supplier_uuid` | `character varying(36)` | NO |  |  |
| `currency` | `character varying(50)` | YES |  |  |
| `item_unit_price` | `numeric(25,12)` | YES |  |  |
| `item_unit_price_str` | `character varying(255)` | YES |  |  |
| `remarks` | `character varying(500)` | YES |  |  |
| `is_manual_record` | `boolean` | YES | false |  |
| `is_deleted` | `boolean` | YES | false |  |
| `pr_uuid` | `character varying(36)` | YES |  |  |
| `serial_number` | `character varying(255)` | YES |  |  |

#### `public.purchase_order`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('purchase_order_id_seq'::regc... | PK |
| `po_global_number` | `character varying(255)` | YES |  |  |
| `po_number` | `character varying(50)` | NO |  |  |
| `pr_number` | `character varying(50)` | YES |  |  |
| `ppo_number` | `character varying(50)` | NO |  |  |
| `po_title` | `character varying(255)` | NO |  |  |
| `status` | `character varying(50)` | YES |  |  |
| `supplier_ack` | `character varying(50)` | YES |  |  |
| `supplier_company_uuid` | `character varying(255)` | YES |  |  |
| `buyer_company_uuid` | `character varying(255)` | YES |  |  |
| `supplier_id` | `bigint(64,0)` | YES |  | FK → `public.suppliers.id` |
| `supplier_address_id` | `bigint(64,0)` | YES |  | FK → `public.addresses.id` |
| `currency_code` | `character varying(20)` | YES |  |  |
| `total_amount` | `numeric(26,2)` | YES |  |  |
| `procurement_type` | `character varying(20)` | YES |  |  |
| `requisition_type` | `character varying(50)` | YES |  |  |
| `requisition_nature` | `character varying(50)` | YES |  |  |
| `submitted_on` | `timestamp with time zone` | YES | now() |  |
| `converted_date` | `timestamp with time zone` | YES |  |  |
| `issued_date` | `timestamp with time zone` | YES |  |  |
| `po_date` | `timestamp with time zone` | YES |  |  |
| `updated_on` | `timestamp with time zone` | YES | now() |  |
| `remark` | `text` | YES |  |  |
| `approval_code_uuid` | `character varying(255)` | YES |  |  |
| `approval_sequence` | `text` | YES |  |  |
| `approval_code` | `character varying(255)` | YES |  |  |
| `next_group` | `character varying(255)` | YES |  |  |
| `requester_name` | `character varying(255)` | YES |  |  |
| `requester_uuid` | `character varying(255)` | YES |  |  |
| `purchaser_name` | `character varying(255)` | YES |  |  |
| `purchaser_uuid` | `character varying(255)` | YES |  |  |
| `payment_terms` | `character varying(255)` | YES |  |  |
| `project_code` | `character varying(50)` | YES |  |  |
| `project_code_uuid` | `character varying(255)` | YES |  |  |
| `project` | `boolean` | YES |  |  |
| `delivery_order_number` | `text` | YES |  |  |
| `global_do_number` | `text` | YES |  |  |
| `do_status` | `character varying(255)` | YES |  |  |
| `uuid` | `character varying(255)` | YES |  |  |
| `has_fully_received` | `boolean` | YES |  |  |
| `buyer_id` | `bigint(64,0)` | YES |  | FK → `public.buyer_information.id` |
| `buyer_contact_person_id` | `bigint(64,0)` | YES |  | FK → `public.contact_person.id` |
| `supplier_contact_person_id` | `bigint(64,0)` | YES |  | FK → `public.contact_person.id` |
| `project_title` | `character varying(1000)` | YES |  |  |
| `original_total_amount` | `numeric(26,2)` | YES | 0 |  |
| `pre_po_id` | `bigint(64,0)` | YES |  | FK → `public.pre_po.id` |
| `currency_name` | `character varying(255)` | YES |  |  |
| `purchase_req_id` | `bigint(64,0)` | YES |  | FK → `public.purchase_req.id` |
| `next_group_uuid` | `character varying(255)` | YES | NULL::character varying |  |
| `rfq_id` | `bigint(64,0)` | YES |  | FK → `public.request_for_quotation.id` |
| `rfq_number` | `character varying(100)` | YES |  |  |
| `tax_amount` | `numeric(26,2)` | YES | 0 |  |
| `sub_total` | `numeric(26,2)` | YES | 0 |  |
| `go_to_approval_route` | `boolean` | YES | false |  |
| `contract_reference_number` | `character varying(500)` | YES |  |  |
| `pre_purchase_req_id` | `bigint(64,0)` | YES |  | FK → `public.pre_purchase_requisition.id` |
| `source_currency_code` | `character varying(255)` | YES |  |  |
| `source_currency_name` | `character varying(255)` | YES |  |  |
| `terms_conditions` | `text` | YES |  |  |
| `delivery_contact_person_id` | `bigint(64,0)` | YES |  | FK → `public.contact_person.id` |
| `is_integration` | `boolean` | YES | false |  |
| `fixed_amount_discount` | `numeric(26,2)` | YES | 0 |  |
| `percentage_discount` | `numeric(26,12)` | YES | 0 |  |
| `is_discount_applied` | `boolean` | YES | false |  |
| `delivery_address_id` | `bigint(64,0)` | YES |  | FK → `public.addresses.id` |
| `request_delivery_date` | `timestamp with time zone` | YES |  |  |
| `payment_terms_uuid` | `character varying(36)` | YES |  |  |
| `po_terms_condition_uuid` | `character varying(150)` | YES |  |  |
| `is_skip_approval_route` | `boolean` | YES | false |  |
| `is_blanket_purchase_order` | `boolean` | YES | false |  |
| `start_date` | `timestamp with time zone` | YES |  |  |
| `end_date` | `timestamp with time zone` | YES |  |  |
| `transaction_type_uuid` | `character varying(255)` | YES |  |  |
| `transaction_type_code` | `character varying(255)` | YES |  |  |
| `transaction_type_name` | `character varying(255)` | YES |  |  |

**Indexes:**
- `purchase_order_buyer_company_uuid_index`: `CREATE INDEX purchase_order_buyer_company_uuid_index ON public.purchase_order USING btree (buyer_company_uuid)`
- `purchase_order_supplier_company_uuid_index`: `CREATE INDEX purchase_order_supplier_company_uuid_index ON public.purchase_order USING btree (supplier_company_uuid)`
- `purchase_order_uuid_index`: `CREATE INDEX purchase_order_uuid_index ON public.purchase_order USING btree (uuid)`
- `unique_buyer_po_number_except_manual`: `CREATE UNIQUE INDEX unique_buyer_po_number_except_manual ON public.purchase_order USING btree (po_number, buyer_company_uuid) WHERE ((po_number)::text IS DISTINCT FROM 'Manual'::text)`

#### `public.purchase_order_audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('purchase_order_audit_trail_i... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(50)` | YES |  |  |
| `status` | `character varying(50)` | YES |  |  |
| `action` | `character varying(100)` | YES |  |  |
| `date_time` | `timestamp with time zone` | NO | now() |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `purchase_order_id` | `bigint(64,0)` | YES |  | FK → `public.purchase_req.id` |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `remark` | `character varying(1000)` | YES |  |  |
| `ref` | `text` | YES |  |  |

#### `public.purchase_req`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('purchase_req_id_seq'::regclass) | PK |
| `is_project` | `boolean` | YES |  |  |
| `pr_number` | `character varying(50)` | YES |  |  |
| `currency_code` | `character varying(50)` | YES |  |  |
| `total_amount` | `numeric(26,2)` | YES |  |  |
| `project_code` | `character varying(50)` | YES |  |  |
| `pr_title` | `character varying(100)` | YES |  |  |
| `procurement_type` | `character varying(50)` | YES |  |  |
| `approval_route_sequence` | `text` | YES |  |  |
| `approval_route_name` | `character varying(100)` | YES |  |  |
| `approval_route_uuid` | `character varying(100)` | YES |  |  |
| `next_approver` | `character varying(255)` | YES |  |  |
| `requestor_uuid` | `character varying(50)` | YES |  |  |
| `requestor_name` | `character varying(255)` | YES |  |  |
| `submitted_date` | `timestamp with time zone` | NO | now() |  |
| `updated_date` | `timestamp with time zone` | NO | now() |  |
| `approved_date` | `timestamp with time zone` | YES |  |  |
| `note` | `text` | YES |  |  |
| `pr_status` | `character varying(255)` | YES |  |  |
| `rfq_process` | `boolean` | YES |  |  |
| `rfq_treshold` | `double precision` | YES |  |  |
| `company_uuid` | `character varying(50)` | YES |  |  |
| `pre_pr_uuid` | `character varying(50)` | YES |  |  |
| `converted_to_ppo` | `boolean` | YES |  |  |
| `pr_global_number` | `character varying(255)` | YES |  |  |
| `uuid` | `character varying(255)` | YES |  |  |
| `next_approval_group` | `character varying(255)` | YES |  |  |
| `project_title` | `character varying(1000)` | YES |  |  |
| `project_uuid` | `character varying(255)` | YES |  |  |
| `currency_name` | `character varying(255)` | YES |  |  |
| `addresses_id` | `bigint(64,0)` | YES |  | FK → `public.addresses.id` |
| `requested_delivery_date` | `timestamp with time zone` | YES |  |  |
| `ppr_id` | `bigint(64,0)` | YES |  | FK → `public.pre_purchase_requisition.id` |
| `delivery_contact_person_id` | `bigint(64,0)` | YES |  | FK → `public.contact_person.id` |
| `is_combination` | `boolean` | YES | false |  |
| `combined_pr_id` | `bigint(64,0)` | YES |  |  |
| `price_comparison_visible` | `boolean` | YES | false |  |
| `transaction_type_uuid` | `character varying(255)` | YES |  |  |
| `transaction_type_code` | `character varying(255)` | YES |  |  |
| `transaction_type_name` | `character varying(255)` | YES |  |  |

**Indexes:**
- `pr_companyuuid_index`: `CREATE INDEX pr_companyuuid_index ON public.purchase_req USING btree (company_uuid)`
- `pr_companyuuid_prnumber_index`: `CREATE INDEX pr_companyuuid_prnumber_index ON public.purchase_req USING btree (company_uuid, pr_number)`
- `pr_companyuuid_prstatus_index`: `CREATE INDEX pr_companyuuid_prstatus_index ON public.purchase_req USING btree (company_uuid, pr_status)`

#### `public.purchase_req_audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('purchase_req_audit_trail_id_... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(50)` | YES |  |  |
| `action` | `character varying(100)` | YES |  |  |
| `date_time` | `timestamp with time zone` | NO | now() |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `purchase_req_id` | `bigint(64,0)` | YES |  | FK → `public.purchase_req.id` |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `remark` | `character varying(1000)` | YES |  |  |
| `po_reference_uuid` | `character varying(100)` | YES |  |  |
| `po_reference_number` | `character varying(50)` | YES |  |  |
| `document_references` | `character varying` | YES |  |  |

**Indexes:**
- `praudittrail_purchasereqid_index`: `CREATE INDEX praudittrail_purchasereqid_index ON public.purchase_req_audit_trail USING btree (purchase_req_id)`

#### `public.purchase_req_conversation`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('purchase_req_conversation_id... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(255)` | YES |  |  |
| `date_time` | `timestamp with time zone` | NO | now() |  |
| `comment` | `character varying(255)` | YES |  |  |
| `external_conversation` | `boolean` | YES |  |  |
| `purchase_req_id` | `bigint(64,0)` | YES |  | FK → `public.purchase_req.id` |

#### `public.purchase_req_document_metadata`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('purchase_req_document_metada... | PK |
| `guid` | `character varying(50)` | YES |  |  |
| `file_label` | `character varying(255)` | YES |  |  |
| `file_description` | `character varying(255)` | YES |  |  |
| `uploaded_on` | `timestamp with time zone` | NO | now() |  |
| `uploaded_by` | `character varying(100)` | YES |  |  |
| `uploader_uuid` | `character varying(50)` | YES |  |  |
| `external_document` | `boolean` | YES |  |  |
| `purchase_req_id` | `bigint(64,0)` | YES |  | FK → `public.purchase_req.id` |
| `file_name` | `character varying(255)` | YES |  |  |

#### `public.purchase_req_item`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('purchase_req_item_id_seq'::r... | PK |
| `item_code` | `character varying(100)` | YES |  |  |
| `item_name` | `character varying(255)` | YES |  |  |
| `item_description` | `text` | YES |  |  |
| `item_model` | `character varying(255)` | YES |  |  |
| `item_size` | `character varying(500)` | YES |  |  |
| `item_brand` | `character varying(255)` | YES |  |  |
| `supplier_name` | `character varying(255)` | YES |  |  |
| `supplier_uuid` | `character varying(50)` | YES |  |  |
| `uom_code` | `character varying(50)` | YES |  |  |
| `source_currency` | `character varying(50)` | YES |  |  |
| `item_unit_price` | `numeric(25,12)` | YES |  |  |
| `item_quantity` | `numeric(25,12)` | YES |  |  |
| `exchange_rate` | `double precision` | YES |  |  |
| `tax_code` | `character varying(50)` | YES |  |  |
| `tax_rate` | `double precision` | YES |  |  |
| `addresses_id` | `bigint(64,0)` | NO |  | FK → `public.addresses.id` |
| `requested_delivery_date` | `timestamp with time zone` | NO | now() |  |
| `gl_account` | `character varying(50)` | YES |  |  |
| `note` | `character varying(3000)` | YES |  |  |
| `purchase_req_id` | `bigint(64,0)` | YES |  | FK → `public.purchase_req.id` |
| `manual_item` | `boolean` | YES |  |  |
| `project_forecast_trade_code` | `character varying(50)` | YES |  |  |
| `company_uuid` | `character varying(50)` | YES |  |  |
| `item_category_uuid` | `character varying(255)` | YES |  |  |
| `item_category` | `character varying(100)` | YES |  |  |
| `price_type` | `character varying(100)` | YES |  |  |
| `contracted` | `boolean` | YES | false |  |
| `contracted_price` | `numeric(25,12)` | YES | 0 |  |
| `contract_reference_number` | `character varying(500)` | YES |  |  |
| `item_uuid` | `character varying(255)` | YES |  |  |
| `item_unit_price_str` | `character varying(255)` | YES | ''::character varying |  |
| `item_quantity_str` | `character varying(255)` | YES | ''::character varying |  |
| `exchange_rate_str` | `character varying(255)` | YES | ''::character varying |  |
| `cat_item_id` | `bigint(64,0)` | YES |  |  |
| `forecast_trade_uuid` | `character varying(255)` | YES |  |  |
| `forecast_trade_label` | `character varying(255)` | YES |  |  |
| `ppr_item_id` | `bigint(64,0)` | YES |  |  |
| `tax_uuid` | `character varying` | YES |  |  |
| `uom_uuid` | `character varying` | YES |  |  |
| `gl_description` | `character varying(255)` | YES |  |  |

**Indexes:**
- `pritem_purchasereqid_index`: `CREATE INDEX pritem_purchasereqid_index ON public.purchase_req_item USING btree (purchase_req_id)`

#### `public.quote`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('quote_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | YES |  |  |
| `currency_code` | `character varying(50)` | YES |  |  |
| `currency_name` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `supplier_uuid` | `character varying(255)` | YES |  |  |
| `request_for_quotation_id` | `bigint(64,0)` | YES |  | FK → `public.request_for_quotation.id` |
| `submitted_date` | `timestamp with time zone` | NO | now() |  |
| `updated_date` | `timestamp with time zone` | NO | now() |  |
| `tax_code` | `character varying(50)` | YES |  |  |
| `non_vendor_company_name` | `character varying(255)` | YES |  |  |
| `manual_quote` | `boolean` | YES | false |  |

**Indexes:**
- `quote_unkey`: `CREATE UNIQUE INDEX quote_unkey ON public.quote USING btree (company_uuid, supplier_uuid, request_for_quotation_id, non_vendor_company_name)`
- `unique_rfq_supplier`: `CREATE UNIQUE INDEX unique_rfq_supplier ON public.quote USING btree (request_for_quotation_id, supplier_uuid)`

#### `public.quote_item`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('quote_item_id_seq'::regclass) | PK |
| `item_code` | `character varying(100)` | YES |  |  |
| `item_name` | `character varying(255)` | YES |  |  |
| `item_description` | `character varying(500)` | YES |  |  |
| `item_model` | `character varying(255)` | YES |  |  |
| `item_size` | `character varying(255)` | YES |  |  |
| `item_brand` | `character varying(255)` | YES |  |  |
| `uom_code` | `character varying(50)` | YES |  |  |
| `currency_code` | `character varying(50)` | YES |  |  |
| `quoted_unit_price` | `numeric(25,12)` | YES |  |  |
| `item_quantity` | `numeric(25,12)` | YES |  |  |
| `exchange_rate` | `double precision` | YES |  |  |
| `tax_code` | `character varying(50)` | YES |  |  |
| `tax_rate` | `double precision` | YES |  |  |
| `note` | `character varying(3000)` | YES |  |  |
| `rfq_item_id` | `bigint(64,0)` | YES |  |  |
| `quote_id` | `bigint(64,0)` | YES |  | FK → `public.quote.id` |
| `buyer_note` | `character varying(3000)` | YES |  |  |
| `awarded_qty` | `numeric(25,12)` | YES |  |  |
| `quoted_date` | `timestamp with time zone` | NO | now() |  |
| `item_unit_price_str` | `character varying(255)` | YES | ''::character varying |  |
| `item_quantity_str` | `character varying(255)` | YES | ''::character varying |  |
| `exchange_rate_str` | `character varying(255)` | YES | ''::character varying |  |
| `cat_item_id` | `bigint(64,0)` | YES |  |  |
| `awarded_qty_str` | `character varying(255)` | YES | ''::character varying |  |
| `tax_uuid` | `character varying` | YES |  |  |

**Indexes:**
- `quoteitem_quote_id_index`: `CREATE INDEX quoteitem_quote_id_index ON public.quote_item USING btree (quote_id)`

#### `public.quote_item_audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('quote_item_audit_trail_id_se... | PK |
| `item_code` | `character varying(100)` | YES |  |  |
| `item_name` | `character varying(255)` | YES |  |  |
| `item_description` | `character varying(500)` | YES |  |  |
| `item_model` | `character varying(255)` | YES |  |  |
| `item_size` | `character varying(255)` | YES |  |  |
| `item_brand` | `character varying(255)` | YES |  |  |
| `uom_code` | `character varying(50)` | YES |  |  |
| `currency_code` | `character varying(50)` | YES |  |  |
| `quoted_unit_price` | `numeric(25,12)` | YES |  |  |
| `item_quantity` | `numeric(25,12)` | YES |  |  |
| `exchange_rate` | `double precision` | YES |  |  |
| `tax_code` | `character varying(50)` | YES |  |  |
| `tax_rate` | `double precision` | YES |  |  |
| `note` | `character varying(3000)` | YES |  |  |
| `quote_item_id` | `bigint(64,0)` | NO |  | FK → `public.quote_item.id` |
| `buyer_note` | `character varying(3000)` | YES |  |  |
| `quoted_date` | `timestamp with time zone` | NO | now() |  |
| `submitted_by` | `character varying(50)` | YES |  |  |
| `item_quantity_str` | `character varying(255)` | YES | ''::character varying |  |
| `quoted_unit_price_str` | `character varying(255)` | YES | ''::character varying |  |
| `exchange_rate_str` | `character varying(255)` | YES | ''::character varying |  |
| `tax_uuid` | `character varying` | YES |  |  |

**Indexes:**
- `quote_item_audit_trail_quote_item_index`: `CREATE INDEX quote_item_audit_trail_quote_item_index ON public.quote_item_audit_trail USING btree (quote_item_id)`

#### `public.request_for_quotation`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('request_for_quotation_id_seq... | PK |
| `rfq_global_number` | `character varying(255)` | YES |  |  |
| `uuid` | `character varying(255)` | YES |  |  |
| `company_uuid` | `character varying(255)` | YES |  |  |
| `rfq_number` | `character varying(255)` | YES |  |  |
| `rfq_type` | `character varying(255)` | YES |  |  |
| `rfq_status` | `character varying(255)` | YES |  |  |
| `pre_pr_uuid` | `character varying(255)` | YES |  |  |
| `is_project` | `boolean` | YES |  |  |
| `currency_code` | `character varying(50)` | YES |  |  |
| `currency_name` | `character varying(255)` | YES |  |  |
| `total_amount` | `numeric(26,2)` | YES |  |  |
| `project_code` | `character varying(50)` | YES |  |  |
| `project_title` | `character varying(255)` | YES |  |  |
| `project_uuid` | `character varying(255)` | YES |  |  |
| `rfq_title` | `character varying(255)` | YES |  |  |
| `procurement_type` | `character varying(50)` | YES |  |  |
| `approval_route_name` | `character varying(255)` | YES |  |  |
| `approval_route_uuid` | `character varying(255)` | YES |  |  |
| `approval_route_sequence` | `text` | YES |  |  |
| `next_approver` | `character varying(255)` | YES |  |  |
| `next_approval_group_uuid` | `character varying(255)` | YES |  |  |
| `requester_uuid` | `character varying(255)` | YES |  |  |
| `requester_name` | `character varying(255)` | YES |  |  |
| `validity_start_date` | `timestamp with time zone` | YES |  |  |
| `validity_end_date` | `timestamp with time zone` | YES |  |  |
| `due_date` | `timestamp with time zone` | YES |  |  |
| `submitted_date` | `timestamp with time zone` | NO | now() |  |
| `updated_date` | `timestamp with time zone` | NO | now() |  |
| `approved_date` | `timestamp with time zone` | YES |  |  |
| `note` | `character varying(3000)` | YES |  |  |
| `converted_to_contract` | `boolean` | YES |  |  |
| `converted_to_purchase` | `boolean` | YES |  |  |
| `pr_uuid` | `character varying(255)` | YES |  |  |
| `delivery_address_id` | `bigint(64,0)` | YES |  | FK → `public.addresses.id` |
| `delivery_date` | `timestamp with time zone` | YES | now() |  |
| `requisition_type` | `character varying(10)` | YES |  |  |
| `total_amount_in_document` | `numeric(26,2)` | NO | 0 |  |
| `contract_number` | `text` | YES |  |  |
| `contract_uuid` | `text` | YES |  |  |
| `pr_id` | `bigint(64,0)` | YES |  |  |
| `delivery_contact_person_id` | `bigint(64,0)` | YES |  | FK → `public.contact_person.id` |
| `transaction_type_uuid` | `character varying(255)` | YES |  |  |
| `transaction_type_code` | `character varying(255)` | YES |  |  |
| `transaction_type_name` | `character varying(255)` | YES |  |  |
| `buyer_id` | `bigint(64,0)` | YES |  |  |
| `company_name` | `character varying(255)` | YES |  |  |
| `is_eoi_enabled` | `boolean` | YES | false |  |

**Indexes:**
- `rfq_companyuuid_index`: `CREATE INDEX rfq_companyuuid_index ON public.request_for_quotation USING btree (company_uuid)`
- `rfq_companyuuid_rfqnumber_index`: `CREATE INDEX rfq_companyuuid_rfqnumber_index ON public.request_for_quotation USING btree (company_uuid, rfq_number)`
- `uq_company_rfq_number`: `CREATE UNIQUE INDEX uq_company_rfq_number ON public.request_for_quotation USING btree (company_uuid, rfq_number)`

#### `public.rfq_audit_trail`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('rfq_audit_trail_id_seq'::reg... | PK |
| `user_name` | `character varying(255)` | YES |  |  |
| `user_role` | `character varying(255)` | YES |  |  |
| `user_uuid` | `character varying(50)` | YES |  |  |
| `action` | `character varying(100)` | YES |  |  |
| `remark` | `character varying(1000)` | YES |  |  |
| `date_time` | `timestamp with time zone` | NO | now() |  |
| `approval_group` | `character varying(255)` | YES |  |  |
| `approval_group_uuid` | `character varying(255)` | YES |  |  |
| `request_for_quotation_id` | `bigint(64,0)` | YES |  | FK → `public.request_for_quotation.id` |
| `supplier_company_uuid` | `character varying(255)` | YES |  |  |
| `rfq_status` | `character varying(255)` | YES |  |  |
| `submitted_by` | `character varying(50)` | YES |  |  |

**Indexes:**
- `rfqaudittrail_rfqid_index`: `CREATE INDEX rfqaudittrail_rfqid_index ON public.rfq_audit_trail USING btree (request_for_quotation_id)`

#### `public.rfq_document_metadata`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('rfq_document_metadata_id_seq... | PK |
| `guid` | `character varying(50)` | YES |  |  |
| `file_label` | `character varying(255)` | YES |  |  |
| `file_description` | `character varying(255)` | YES |  |  |
| `uploaded_on` | `timestamp with time zone` | NO | now() |  |
| `uploaded_by` | `character varying(100)` | YES |  |  |
| `uploader_uuid` | `character varying(50)` | YES |  |  |
| `external_document` | `boolean` | YES |  |  |
| `request_for_quotation_id` | `bigint(64,0)` | YES |  | FK → `public.request_for_quotation.id` |
| `supplier_company_uuid` | `character varying(255)` | YES |  |  |
| `rfq_status` | `character varying(255)` | YES |  |  |
| `file_name` | `character varying(255)` | YES |  |  |

**Indexes:**
- `rfq_document_metadata_rfqid_index`: `CREATE INDEX rfq_document_metadata_rfqid_index ON public.rfq_document_metadata USING btree (request_for_quotation_id)`

#### `public.rfq_email_access`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('rfq_email_access_id_seq'::re... | PK |
| `rfq_uuid` | `character varying(255)` | YES |  |  |
| `supplier_uuid` | `character varying(255)` | NO |  |  |
| `supplier_contact_email` | `character varying(255)` | NO |  |  |
| `token` | `character varying(1000)` | YES |  |  |
| `created_at` | `timestamp with time zone` | YES |  |  |
| `expired_at` | `timestamp with time zone` | YES |  |  |
| `used` | `boolean` | YES | false |  |
| `non_vendor_company_name` | `character varying(255)` | YES |  |  |

**Indexes:**
- `rfq_email_access_id_uindex`: `CREATE UNIQUE INDEX rfq_email_access_id_uindex ON public.rfq_email_access USING btree (id)`

#### `public.rfq_item`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('rfq_item_id_seq'::regclass) | PK |
| `item_code` | `character varying(100)` | YES |  |  |
| `item_name` | `character varying(255)` | YES |  |  |
| `item_description` | `character varying(500)` | YES |  |  |
| `item_model` | `character varying(255)` | YES |  |  |
| `item_size` | `character varying(500)` | YES |  |  |
| `item_brand` | `character varying(255)` | YES |  |  |
| `item_category` | `character varying(255)` | YES |  |  |
| `item_category_uuid` | `character varying(255)` | YES |  |  |
| `supplier_name` | `character varying(255)` | YES |  |  |
| `supplier_uuid` | `character varying(255)` | YES |  |  |
| `uom_code` | `character varying(50)` | YES |  |  |
| `source_currency` | `character varying(50)` | YES |  |  |
| `item_unit_price` | `numeric(25,12)` | YES |  |  |
| `item_quantity` | `numeric(25,12)` | YES |  |  |
| `exchange_rate` | `double precision` | YES |  |  |
| `tax_code` | `character varying(50)` | YES |  |  |
| `tax_rate` | `double precision` | YES |  |  |
| `addresses_id` | `bigint(64,0)` | NO |  | FK → `public.addresses.id` |
| `requested_delivery_date` | `timestamp with time zone` | NO | now() |  |
| `note` | `character varying(3000)` | YES |  |  |
| `manual_item` | `boolean` | YES |  |  |
| `project_forecast_trade_code` | `character varying(50)` | YES |  |  |
| `company_uuid` | `character varying(50)` | YES |  |  |
| `request_for_quotation_id` | `bigint(64,0)` | YES |  | FK → `public.request_for_quotation.id` |
| `gl_account_number` | `character varying(50)` | YES |  |  |
| `item_unit_price_str` | `character varying(255)` | YES | ''::character varying |  |
| `item_quantity_str` | `character varying(255)` | YES | ''::character varying |  |
| `exchange_rate_str` | `character varying(255)` | YES | ''::character varying |  |
| `cat_item_id` | `bigint(64,0)` | YES |  |  |
| `forecast_trade_uuid` | `character varying(255)` | YES |  |  |
| `forecast_trade_label` | `character varying(255)` | YES |  |  |
| `uom_uuid` | `character varying` | YES |  |  |

**Indexes:**
- `rfqitem_rfqid_index`: `CREATE INDEX rfqitem_rfqid_index ON public.rfq_item USING btree (request_for_quotation_id)`

#### `public.rfq_negotiation`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('rfq_negotiation_id_seq'::reg... | PK |
| `guid` | `character varying(50)` | YES |  |  |
| `file_label` | `character varying(100)` | YES |  |  |
| `comment` | `character varying(500)` | YES |  |  |
| `uploaded_on` | `timestamp with time zone` | NO | now() |  |
| `uploaded_by` | `character varying(100)` | YES |  |  |
| `uploader_uuid` | `character varying(100)` | YES |  |  |
| `uploader_role` | `character varying(100)` | YES |  |  |
| `request_for_quotation_id` | `bigint(64,0)` | YES |  | FK → `public.request_for_quotation.id` |
| `supplier_uuid` | `character varying(255)` | YES |  |  |

**Indexes:**
- `rfq_negotiation_rfqid_index`: `CREATE INDEX rfq_negotiation_rfqid_index ON public.rfq_negotiation USING btree (request_for_quotation_id)`

#### `public.rfq_non_vendor`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('rfq_non_vendor_id_seq'::regc... | PK |
| `company_name` | `character varying(255)` | NO |  |  |
| `contact_person_name` | `character varying(255)` | YES |  |  |
| `contact_person_email` | `character varying(255)` | NO |  |  |
| `request_for_quotation_id` | `bigint(64,0)` | NO |  | FK → `public.request_for_quotation.id` |
| `quote_id` | `bigint(64,0)` | YES |  | FK → `public.quote.id` |
| `supplier_uuid` | `character varying(255)` | YES |  |  |

#### `public.rfq_vendor`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('rfq_vendor_id_seq'::regclass) | PK |
| `request_for_quotation_id` | `bigint(64,0)` | YES |  | FK → `public.request_for_quotation.id` |
| `supplier_id` | `bigint(64,0)` | YES |  | FK → `public.suppliers.id` |
| `supplier_company_uuid` | `character varying(255)` | YES |  |  |
| `quote_id` | `bigint(64,0)` | YES |  | FK → `public.quote.id` |

#### `public.sequence_generator`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('sequence_generator_id_seq'::... | PK |
| `company_uuid` | `character varying(50)` | YES |  |  |
| `type` | `character varying(50)` | NO |  |  |
| `number` | `character varying(50)` | NO |  |  |

**Indexes:**
- `uq_company_uuid_type`: `CREATE UNIQUE INDEX uq_company_uuid_type ON public.sequence_generator USING btree (company_uuid, type)`

#### `public.suppliers`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('suppliers_id_seq'::regclass) | PK |
| `uuid` | `character varying(255)` | NO |  |  |
| `code` | `character varying(255)` | NO |  |  |
| `company_name` | `character varying(255)` | NO |  |  |
| `contact_person_name` | `character varying(255)` | NO |  |  |
| `contact_person_email` | `character varying(255)` | NO |  |  |
| `contact_person_work_number` | `character varying(50)` | NO |  |  |
| `country_code` | `character varying(255)` | YES |  |  |
| `company_registration_no` | `character varying(50)` | YES |  |  |
| `country_of_origin` | `character varying(255)` | YES |  |  |
| `md5check_sum` | `character varying(255)` | YES |  |  |

**Indexes:**
- `supplier_uuid_index`: `CREATE INDEX supplier_uuid_index ON public.suppliers USING btree (uuid)`

#### `public.test`

- **Type:** BASE TABLE  **Rows:** N/A

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| `id` | `bigint(64,0)` | NO | nextval('test_id_seq'::regclass) | PK |
| `purchase_req_id` | `bigint(64,0)` | YES |  | FK → `public.purchase_req.id` |
| `name` | `character varying` | YES |  |  |

---
