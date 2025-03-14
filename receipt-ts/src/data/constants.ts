import { CurrencyDirectory, CompanyDirectory, CategoryItems } from '../types/types';

export const CURRENCIES: CurrencyDirectory = {
  "MYR": { symbol: "RM", rate: 1.0, name: "Malaysian Ringgit" },
  "BHD": { symbol: "BD", rate: 0.083, name: "Bahraini Dinar" },
  "INR": { symbol: "₹", rate: 17.25, name: "Indian Rupee" },
  "USD": { symbol: "$", rate: 0.21, name: "US Dollar" },
  "EUR": { symbol: "€", rate: 0.19, name: "Euro" }
};

export const PAYMENT_METHODS = [
  "CASH",
  "VISA ****1234",
  "MASTERCARD ****5678",
  "AMEX ****9012",
  "E-WALLET",
  "MOBILE PAY"
];

export const STORE_LOCATIONS = [
  "Downtown Mall #123",
  "Westside Plaza #456",
  "Eastside Market #789",
  "North Station #321",
  "South Center #654",
  "Central Square #987",
  "Harbor View #147",
  "University District #258",
  "Suburban Market #369",
  "Metro Express #741",
  "BERJAYA COFFEE #875",
  "STARCITY CAFE #654",
  "COFFEE HOUSE #432"
];

export const COMPANY_INFO: CompanyDirectory = {
  "BERJAYA COFFEE": {
    company_name: "BERJAYA STARBUCKS COFFEE COMPANY SDN BHD",
    legal_name: "BERJAYA FOOD TRADING SDN BHD",
    tax_id: "GST ID: 001234567890",
    service_tax_id: "SERVICE TAX ID: WID-1558-31025875",
    company_number: "Company No. 157251-A",
    halal_cert: "HALAL CERT: JAKIM-HD28185",
    business_license: "LICENSE: KL-2024-123456",
    food_license: "FOOD LICENSE: FL-789012",
    address: "Level 15, West Wing, Berjaya Times Square\n1, Jalan Imbi, 55100 Kuala Lumpur, Malaysia",
    phone: "Tel: 1-300-80-8888",
    fax: "Fax: +603-2141-0555",
    website: "www.starbucks.com.my",
    email: "customerservice@starbucks.com.my",
    currency: "MYR",
    region: "MY-14",
    store_type: "FLAGSHIP STORE",
    tax_rate: 0.06,
    service_charge: 0.10
  },
  "STARCITY CAFE": {
    company_name: "STARCITY COFFEE & BEVERAGES PTE LTD",
    legal_name: "STARCITY HOLDINGS PTE LTD",
    tax_id: "GST REG: M8-0123456-7",
    service_tax_id: "SERVICE TAX ID: SCC-2558-41025875",
    company_number: "UEN: 202312345K",
    halal_cert: "HALAL CERT: MUIS-HC-N23-2024",
    business_license: "LICENSE: SG-2024-78901",
    food_license: "NEA LICENSE: FE2023-12345",
    address: "123 City Plaza\n#01-23 Singapore 123456",
    phone: "Tel: +65 6789 0123",
    fax: "Fax: +65 6789 0124",
    website: "www.starcity.com.sg",
    email: "info@starcity.com.sg",
    currency: "BHD",
    region: "SG-05",
    store_type: "PREMIUM OUTLET",
    tax_rate: 0.08,
    service_charge: 0.12
  },
  "COFFEE HOUSE": {
    company_name: "COFFEE HOUSE INTERNATIONAL LLC",
    legal_name: "GLOBAL BEVERAGES HOLDINGS INC.",
    tax_id: "TAX ID: 98-7654321",
    service_tax_id: "FOOD SERVICE LICENSE: FSL-3558-51025875",
    company_number: "Business Reg: BRN-55512345",
    halal_cert: "HALAL CERT: HMC-2024-789",
    business_license: "LICENSE: CA-2024-456789",
    food_license: "FDA: FD-123-456-789",
    address: "888 Coffee Street\nSuite 100, Beverly Hills, CA 90210",
    phone: "Tel: (888) COFFEE-1",
    fax: "Fax: (888) COFFEE-2",
    website: "www.coffeehouse.com",
    email: "support@coffeehouse.com",
    currency: "USD",
    region: "US-CA",
    store_type: "CONCEPT STORE",
    tax_rate: 0.0925,
    service_charge: 0.15
  }
}; 