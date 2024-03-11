import { getUnitDisplay } from "@/lib/utils";
import { expect, describe, beforeEach, it, vi } from "vitest";

const UNIT = {
  code: "nr_hab",
  alt_label: "habitants",
  label: "Number of habitants",
};
const UNIT_PC_1 = {
  code: "pc_hab",
  alt_label: "% of habitants",
  label: "Percentage of habitants",
};
const UNIT_PC_2 = {
  code: "hab_score",
  alt_label: "% of habitants",
  label: "Percentage of habitants",
};

function checkDisplayUnit(value, valueStr) {
  expect(getUnitDisplay(value, UNIT)).toBe(valueStr + " habitants");
}

function checkDisplayUnitPercent(value, valueStr) {
  expect(getUnitDisplay(value, UNIT_PC_1)).toBe(valueStr + "% of habitants");
  expect(getUnitDisplay(value, UNIT_PC_2)).toBe(valueStr + "% of habitants");
}

// See Rounding Modes in Number format for details on how this should work:
// We're using the default, since there is no browser support for other versions at this time.
//  https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat#rounding_modes
describe("check unit display", () => {
  beforeEach(() => {
    vi.mock("@/stores/chartStore", () => {
      return {
        useChartStore() {
          return { currentChart: {} };
        },
      };
    });
  });
  // Percentage display have special rules
  it("check unit percentage", () => {
    checkDisplayUnitPercent(0.123456789, "0.12");
    checkDisplayUnitPercent(1.23456789, "1.23");
    checkDisplayUnitPercent(12.3456789, "12.35");
    checkDisplayUnitPercent(123.456789, "123.46");
  });
  it("check value < 1K", () => {
    checkDisplayUnit(0.124, "0.124");
    checkDisplayUnit(0.1249, "0.1249");
    checkDisplayUnit(0.125, "0.125");
    checkDisplayUnit(1.234, "1.234");
    checkDisplayUnit(12.34, "12.34");
    checkDisplayUnit(12.3456789, "12.3456789");
    checkDisplayUnit(123.4, "123");
  });
  it("check 1K < value < 1M", () => {
    checkDisplayUnit(1234.1, "1,234");
    checkDisplayUnit(1234.5, "1,235");
    checkDisplayUnit(12345.1, "12,345");
    checkDisplayUnit(12345.5, "12,346");
    checkDisplayUnit(123456.1, "123,456");
    checkDisplayUnit(123456.5, "123,457");
  });
  it("check 1M < value < 1B", () => {
    checkDisplayUnit(1234567, "1.23M");
    checkDisplayUnit(12345678, "12.35M");
    checkDisplayUnit(123456789, "123.46M");
  });
  it("check value > 1B", () => {
    checkDisplayUnit(1234567890, "1.23B");
    checkDisplayUnit(12345678901, "12.35B");
  });
});
