import os
from playwright.async_api import Playwright, async_playwright, Error, Page
import asyncio
from .encryptPass import password, user, url, company
import pandas as pd
from dataHandle.data import format_data

wait_time = 1500  # 60000 = 1min so units are in milliseconds
download_time = 30000  # 60000 = 1min so units are in milliseconds


async def safe_goto(page: Page, url: str, max_retries=10, delay=0.5):
    """Function to safely go to a specific url using playwright
    This fixes the issue where you may not connect to the address
    on the first try. This will try about 10 times until you can connect"""
    for attempt in range(1, max_retries + 1):
        try:
            response = await page.goto(url)
            print("Navigation successful!")
            return response  # or perform further actions with the response
        except Error as e:
            # Check if the error message indicates a DNS resolution issue
            if "net::ERR_NAME_NOT_RESOLVED" in str(e):
                print(
                    f"Attempt {attempt} failed with error: {e}. Retrying in {delay} second(s)..."
                )
                await asyncio.sleep(delay)
            else:
                # If it's a different error, re-raise it
                raise
    # If all attempts fail, you can choose to raise an exception or handle it gracefully
    raise Exception(f"Failed to navigate to {url} after {max_retries} attempts.")


async def login_e2(page: Page):
    """Function to log into E2 and this will use the seperate module encryptPass
    for checking if a user name and password exists if not then it will
    prompt the user to create one for their E2 account"""
    await page.get_by_role("textbox", name="").fill(user())
    await page.get_by_role("textbox", name="").fill(password())
    await page.get_by_role("button", name=" LOGIN").click()
    await page.locator("#company").select_option(company())
    await page.get_by_role("link", name="Main").click()
    try:
        await page.get_by_text("This user is already logged").click(timeout=2000)
        await page.get_by_role("button", name=" Yes").click()
    except Error as e:
        if "Timeout" in str(e):
            pass


async def logout_e2(page: Page):
    """Function to log out of E2, right now it only works for username max and
    this needs to be made more general for everyone"""
    await page.locator("span.user-info.hidden-xs").click()
    await page.locator("#navbar-container").get_by_text("Logout").click()


async def uncheck(page: Page, locationName: str):
    """Function to uncheck a checkbox element on E2
    This function first tries to find the element using the locator function
    if that does not work it will use the get_by_text function"""
    checkbox = page.locator(locationName)
    if await checkbox.count() == 0:
        checkbox = page.get_by_text(locationName)
    if await checkbox.is_checked():
        await checkbox.click()


async def getmfg(page: Page):
    """Function to take mfg cost info from a job details page"""
    job_number_box = page.locator("#cg_tbJobNumber div")
    part_number_box = page.locator("#cg_tbPartNumber div")
    customer_box = page.locator("#cg_tbCustomer div")
    product_code_box = page.locator("#cg_tbProductCode")
    mfg_box = page.locator("#cg_curUDCurrency2 div").nth(1)
    plt1_box = page.locator("#cg_tbUDNumber1 div").nth(1)
    plt2_box = page.locator("#cg_tbUDNumber2 div").nth(1)
    plt6_box = page.locator("#cg_tbUDNumber3 div").nth(1)
    plt7_box = page.locator("#cg_tbUDNumber4 div").nth(1)
    total_qty_box = page.locator("#cg_numQtyOrdered div").nth(1)
    await job_number_box.click(click_count=3)
    job_number = await page.evaluate("() => window.getSelection().toString()")
    await part_number_box.click(click_count=3)
    part_number = await page.evaluate("() => window.getSelection().toString()")
    await customer_box.click(click_count=3)
    customer = await page.evaluate("() => window.getSelection().toString()")
    await product_code_box.click(click_count=3)
    product_code = await page.evaluate("() => window.getSelection().toString()")
    await mfg_box.click(click_count=3)
    mfg = await page.evaluate("() => window.getSelection().toString()")
    mfg = float(mfg.replace("$", "").replace(",", ""))
    await plt1_box.click(click_count=3)
    plt1 = await page.evaluate("() => window.getSelection().toString()")
    await plt2_box.click(click_count=3)
    plt2 = await page.evaluate("() => window.getSelection().toString()")
    await plt6_box.click(click_count=3)
    plt6 = await page.evaluate("() => window.getSelection().toString()")
    await plt7_box.click(click_count=3)
    plt7 = await page.evaluate("() => window.getSelection().toString()")
    await total_qty_box.click(click_count=3)
    total_qty = await page.evaluate("() => window.getSelection().toString()")
    total_qty = total_qty.replace(",", "")
    mfg_total = float(total_qty) * mfg
    plt1_total = 0.0
    hs_total = 0.0
    plt2_total = 0.0
    plt6_total = 0.0
    plt7_total = 0.0
    if plt1 != "" and "RESALE" in product_code:
        hs_total = round(mfg_total * float(plt1) * 0.01, 2)
    if plt1 != "" and "RESALE" not in product_code:
        plt1_total = round(mfg_total * float(plt1) * 0.01, 2)
    if plt2 != "":
        plt2_total = round(mfg_total * float(plt2) * 0.01, 2)
    if plt6 != "":
        plt6_total = round(mfg_total * float(plt6) * 0.01, 2)
    if plt7 != "":
        plt7_total = round(mfg_total * float(plt7) * 0.01, 2)
    data = {
        "Job Number": [job_number],
        "Customer": [customer],
        "Part Number": [part_number],
        "HS": [hs_total],
        "Plt #1": [plt1_total],
        "Plt #2": [plt2_total],
        "Plt #6": [plt6_total],
        "Plt #7": [plt7_total],
    }
    totals = pd.DataFrame(data)
    await page.get_by_role("button", name=" Close").click()
    return totals


async def get_grid_rows(page: Page, locator_id: str, column_name: str) -> pd.Series:
    """Function to get grid data for the line items of a job inquiry"""
    download_name = (
        os.path.abspath(".") + "/assets/temp_data/" + "lineItem-GridExport.xlsx"
    )
    try:
        async with page.expect_download(timeout=download_time) as download_info:
            await page.locator(locator_id).click()
        download = await download_info.value
        await download.save_as(download_name)
    except Error as e:
        print(e)
        raise
    df = pd.read_excel(download_name, dtype="string")
    os.remove(download_name)
    return df[column_name]


async def loopThroughLineItems(page):
    customer_box = page.locator("#cg_tbCustomer div")
    await customer_box.click(click_count=3)
    customer = await page.evaluate("() => window.getSelection().toString()")
    if "STOCK" in customer or "COLE CARBIDE" in customer:
        await page.get_by_role("button", name=" Close").click()
        return pd.DataFrame()

    job_number_box = page.locator("#st-header-text")
    await job_number_box.click(click_count=3)
    job_number = await page.evaluate("() => window.getSelection().toString()")
    job_number = (
        job_number.replace("Job Status Inquiry : ", "")
        .replace("quick view", "")
        .strip()
    )
    columns = [
        "Job Number",
        "Customer",
        "Part Number",
        "HS",
        "Plt #1",
        "Plt #2",
        "Plt #6",
        "Plt #7",
    ]
    totals = pd.DataFrame(columns=columns)
    await page.wait_for_selector(".tabulator-row")
    rows = await get_grid_rows(page, "#btnPrint_gvOrderDetailsGrid", "Job Number")
    for row_id in range(len(rows)):
        try:
            row_name = rows.iloc[row_id]
            await page.get_by_role("gridcell", name=row_name).click(timeout=wait_time)
            await page.get_by_role("button", name=" Details").click()
            temp_total = await getmfg(page)
            totals = pd.concat([totals if not totals.empty else None, temp_total])
        except Error as e:
            if "timeout" in str(e):
                if row_id == 1:
                    return pd.DataFrame()
            else:
                print(e)
                raise
    await page.get_by_role("button", name=" Close").click()
    return totals


async def set_asc_sort(sort_locator):
    sort_value = await sort_locator.get_attribute("aria-sort")
    while sort_value != "asc":
        await sort_locator.click()
        sort_value = await sort_locator.get_attribute("aria-sort")


async def loopThroughJobs(page: Page):
    """Function to loop through all job status jobs with the date
    requested as user input"""
    mfgDate = input("Please input the MFG$ date : ")
    await page.get_by_role("button", name="").click()
    await page.get_by_role("link", name=" Job Status").click()
    await page.get_by_role("textbox", name="Search For").click()
    await page.get_by_role("textbox", name="Search For").fill("")
    await page.locator(".input-group-addon > .ace-icon").click()
    await page.locator('input[name="daterangepicker_start"]').nth(1).click()
    await page.locator('input[name="daterangepicker_start"]').nth(1).fill(mfgDate)
    await page.locator('input[name="daterangepicker_end"]').nth(1).click()
    await page.locator('input[name="daterangepicker_end"]').nth(1).fill(mfgDate)
    await page.get_by_role("button", name="Apply").click()
    await page.get_by_role("button", name=" Search").click()
    sort_locator = page.get_by_role("columnheader", name="Order ")
    await set_asc_sort(sort_locator)
    await page.wait_for_selector(".tabulator-row")
    rows = await get_grid_rows(page, "#btnPrint_grdResults", "Order")
    columns = [
        "Job Number",
        "Customer",
        "Part Number",
        "HS",
        "Plt #1",
        "Plt #2",
        "Plt #6",
        "Plt #7",
    ]
    totals = pd.DataFrame(columns=columns)
    temp_totals = pd.DataFrame(columns=columns)
    for row_id in range(len(rows)):
        try:
            row_name = rows.iloc[row_id]
            await page.get_by_role("gridcell", name=row_name).click(timeout=wait_time)
            await page.get_by_role("button", name=" View").click()
            temp_totals = await loopThroughLineItems(page)
            if not temp_totals.empty:
                totals = pd.concat([totals if not totals.empty else None, temp_totals])
            await set_asc_sort(sort_locator)
        except Error as e:
            if "Timeout" in str(e):
                pass
            else:
                print(e)
                raise
    await page.get_by_role("button", name=" Close").click()
    hs_total = totals["HS"].sum()
    plt1_total = totals["Plt #1"].sum()
    plt2_total = totals["Plt #2"].sum()
    plt6_total = totals["Plt #6"].sum()
    plt7_total = totals["Plt #7"].sum()
    grand_total = plt1_total + plt2_total + plt6_total + plt7_total
    data = {
        "Job Number": [""],
        "Customer": ["Plant Totals"],
        "Part Number": [grand_total],
        "HS": [hs_total],
        "Plt #1": [plt1_total],
        "Plt #2": [plt2_total],
        "Plt #6": [plt6_total],
        "Plt #7": [plt7_total],
    }
    temp_totals = pd.DataFrame(data)
    totals = pd.concat([totals if not totals.empty else None, temp_totals])
    totals = totals.set_index("Job Number")
    format_data(totals)


async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(
        headless=False,
    )
    page = await browser.new_page()
    try:
        await safe_goto(page, url(), 10)
    except Exception as e:
        print(e)
    await login_e2(page)
    try:
        await loopThroughJobs(page)
        await logout_e2(page)
    except Error as e:
        print(e)
        await logout_e2(page)
    # ---------------------
    await browser.close()


async def main_playwright():
    async with async_playwright() as playwright:
        await run(playwright)


def download_data():
    asyncio.run(main_playwright())
