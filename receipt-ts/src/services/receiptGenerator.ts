import { ReceiptData, ReceiptItem, Currency, CompanyInfo } from '../types/types';
import { CURRENCIES, PAYMENT_METHODS, STORE_LOCATIONS, COMPANY_INFO } from '../data/constants';

let currentStoreLocation: string;

function getCompanyType(storeLocation: string): string | null {
  if (storeLocation.includes("BERJAYA")) return "BERJAYA COFFEE";
  if (storeLocation.includes("STARCITY")) return "STARCITY CAFE";
  if (storeLocation.includes("COFFEE HOUSE")) return "COFFEE HOUSE";
  return null;
}

function formatCurrency(amount: number, currencyInfo: Currency): string {
  const converted = amount * currencyInfo.rate;
  return `${currencyInfo.symbol}${converted.toFixed(2)}`;
}

function generateRandomId(prefix: string, min: number, max: number): string {
  return `${prefix}${Math.floor(Math.random() * (max - min + 1) + min)}`;
}

export function generateReceipt(): ReceiptData & {
  timestamp: string;
  store_id: string;
  service_id: string;
  company_info?: CompanyInfo;
  receipt_number: string;
  employee_id: string;
  shift_id: string;
  pos_id: string;
} {
  // Select random store location
  currentStoreLocation = STORE_LOCATIONS[Math.floor(Math.random() * STORE_LOCATIONS.length)];
  
  const receiptItems: ReceiptItem[] = [];
  let total = 0;
  
  // Get company info and currency
  const companyType = getCompanyType(currentStoreLocation);
  const storeInfo = companyType ? COMPANY_INFO[companyType] : undefined;
  
  // Select currency
  const currencyCode = storeInfo ? storeInfo.currency : Object.keys(CURRENCIES)[Math.floor(Math.random() * Object.keys(CURRENCIES).length)];
  const currencyInfo = CURRENCIES[currencyCode];
  
  // Check if it's a cafe location
  const isCafe = currentStoreLocation.includes("COFFEE") || currentStoreLocation.includes("CAFE") || currentStoreLocation.includes("BERJAYA");
  
  // Generate items (simplified for this example)
  const numItems = isCafe ? Math.floor(Math.random() * 4) + 1 : Math.floor(Math.random() * 15) + 5;
  
  for (let i = 0; i < numItems; i++) {
    const quantity = Math.floor(Math.random() * (isCafe ? 3 : 5)) + 1;
    const price = Math.random() * 10 + 2; // Random price between 2 and 12
    const itemTotal = quantity * price;
    total += itemTotal;
    
    receiptItems.push({
      category: isCafe ? "Cafe & Coffee" : "General",
      name: isCafe ? `Coffee Item ${i + 1}` : `Item ${i + 1}`,
      quantity,
      price: formatCurrency(price, currencyInfo),
      total: formatCurrency(itemTotal, currencyInfo)
    });
  }
  
  // Calculate charges
  const serviceChargeRate = storeInfo ? storeInfo.service_charge : 0;
  const taxRate = storeInfo ? storeInfo.tax_rate : 0.06;
  const serviceCharge = isCafe ? total * serviceChargeRate : 0;
  const tax = (total + serviceCharge) * taxRate;
  const finalTotal = total + serviceCharge + tax;
  
  // Generate receipt data
  const timestamp = new Date().toLocaleString();
  const receiptNumber = `${new Date().getFullYear()}${String(new Date().getMonth() + 1).padStart(2, '0')}${String(new Date().getDate()).padStart(2, '0')}-${Math.floor(Math.random() * 9000) + 1000}`;
  
  return {
    items: receiptItems,
    subtotal: formatCurrency(total, currencyInfo),
    service_charge: formatCurrency(serviceCharge, currencyInfo),
    tax: formatCurrency(tax, currencyInfo),
    total: formatCurrency(finalTotal, currencyInfo),
    currency_info: currencyInfo,
    payment_method: PAYMENT_METHODS[Math.floor(Math.random() * PAYMENT_METHODS.length)],
    terminal_id: generateRandomId("TERM", 100, 999),
    merchant_id: generateRandomId("MID", 10000, 99999),
    batch_no: Math.floor(Math.random() * 999) + 1,
    trace_no: Math.floor(Math.random() * 900000) + 100000,
    timestamp,
    store_id: currentStoreLocation,
    service_id: `WID-${Math.floor(Math.random() * 9000) + 1000}-${Math.floor(Math.random() * 90000000) + 10000000}`,
    company_info: storeInfo,
    receipt_number: receiptNumber,
    employee_id: generateRandomId("EMP", 1000, 9999),
    shift_id: `SHIFT-${Math.floor(Math.random() * 3) + 1}`,
    pos_id: `POS-${String(Math.floor(Math.random() * 99) + 1).padStart(2, '0')}`
  };
} 