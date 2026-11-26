import pkg from "@/package.json";

/**
 * Versi aplikasi, dibaca dari package.json supaya tidak ada angka yang di-hardcode.
 */
export const APP_VERSION: string = pkg.version;
