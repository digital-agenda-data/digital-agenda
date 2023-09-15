import { getUnitDisplay } from "@/lib/utils";
import { expect, test } from "vitest";

const UNIT = { code: "nr_hab", display: "Number of habitants" };
const UNIT_PC = { code: "pc_hab", display: "% of habitants" };

function checkDisplayUnit(value, valueStr) {
  expect(getUnitDisplay(value, UNIT)).toBe(valueStr + " Number of habitants");
}

function checkDisplayUnitPercent(value, valueStr) {
  expect(getUnitDisplay(value, UNIT_PC)).toBe(valueStr + "% of habitants");
}

// See Rounding Modes in Number format for details on how this should work:
// We're using the default, since there is no browser support for other versions at this time.
//  https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat#rounding_modes
test("displayUnit", () => {
  checkDisplayUnitPercent(0.123456789, "0.12");
  checkDisplayUnitPercent(1.23456789, "1.23");
  checkDisplayUnitPercent(12.3456789, "12.35");
  checkDisplayUnitPercent(123.456789, "123.46");

  checkDisplayUnit(0.124, "0.124");
  checkDisplayUnit(0.1249, "0.1249");
  checkDisplayUnit(0.125, "0.125");
  checkDisplayUnit(1.234, "1.234");
  checkDisplayUnit(12.34, "12.34");
  checkDisplayUnit(12.3456789, "12.3456789");
  checkDisplayUnit(123.4, "123");

  checkDisplayUnit(1234.1, "1,234");
  checkDisplayUnit(1234.5, "1,235");
  checkDisplayUnit(12345.1, "12,345");
  checkDisplayUnit(12345.5, "12,346");
  checkDisplayUnit(123456.1, "123,456");
  checkDisplayUnit(123456.5, "123,457");

  checkDisplayUnit(1234567, "1.23M");
  checkDisplayUnit(12345678, "12.35M");
  checkDisplayUnit(123456789, "123.46M");

  checkDisplayUnit(1234567890, "1.23B");
  checkDisplayUnit(12345678901, "12.35B");
});
