export interface Currency {
  symbol: string;
  rate: number;
  name: string;
}

export interface CompanyInfo {
  company_name: string;
  legal_name: string;
  tax_id: string;
  service_tax_id: string;
  company_number: string;
  halal_cert: string;
  business_license: string;
  food_license: string;
  address: string;
  phone: string;
  fax: string;
  website: string;
  email: string;
  currency: string;
  region: string;
  store_type: string;
  tax_rate: number;
  service_charge: number;
}

export interface ReceiptItem {
  category: string;
  name: string;
  quantity: number;
  price: string;
  total: string;
}

export interface ReceiptData {
  items: ReceiptItem[];
  subtotal: string;
  service_charge: string;
  tax: string;
  total: string;
  currency_info: Currency;
  payment_method: string;
  terminal_id: string;
  merchant_id: string;
  batch_no: number;
  trace_no: number;
}

export interface ItemPriceRange {
  [key: string]: [number, number];
}

export interface CategoryItems {
  [key: string]: ItemPriceRange;
}

export interface CompanyDirectory {
  [key: string]: CompanyInfo;
}

export interface CurrencyDirectory {
  [key: string]: Currency;
} 