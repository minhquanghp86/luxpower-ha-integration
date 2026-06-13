# Tích hợp LuxPower Modbus cho Home Assistant
# Đây là bản dịch sang Tiếng Việt dựa trên repo gốc https://github.com/ant0nkr/luxpower-ha-integration

[![HACS Default](https://img.shields.io/badge/HACS-Default-blue.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/ant0nkr/luxpower-ha-integration?style=for-the-badge)](https://github.com/ant0nkr/luxpower-ha-integration/releases)
[![GitHub License](https://img.shields.io/github/license/ant0nkr/luxpower-ha-integration?style=for-the-badge)](https://github.com/ant0nkr/luxpower-ha-integration/blob/main/LICENSE)
[![Donate](https://img.shields.io/badge/Donate-PayPal-yellow.svg?style=for-the-badge)](https://www.paypal.com/donate/?business=LDZNJ5UTHRBY8&no_recurring=0&item_name=Help+improve+Lux+Power+integration+for+Home+Assistant.+Every+contribution+keeps+the+project+alive&currency_code=USD)

Một tích hợp toàn diện cho Home Assistant để giám sát và điều khiển biến tần LuxPower thông qua giao diện Modbus TCP.

Tích hợp này kết nối trực tiếp với dongle WiFi của biến tần, cung cấp dữ liệu thời gian thực và khả năng điều khiển nhiều thiết lập mà không cần phụ thuộc vào cloud.

> [!NOTE]
> **Phiên bản 1.0.0** mang đến một cuộc cải tổ kiến trúc lớn, hơn 140 thực thể mới, và **giám sát BMS pin** với tự động phát hiện. Xem [phần Giám sát Pin](#giám-sát-pin-có-từ-phiên-bản-v100) dưới đây để biết chi tiết.

## Tính năng

* **Giám sát thời gian thực:** Theo dõi công suất PV, trạng thái sạc pin (SOC), nhập/xuất lưới điện, công suất tải, và nhiều thông số khác.
* **Điều khiển biến tần:** Thay đổi dòng sạc/xả, đặt lịch sạc/xả theo thời gian, và bật/tắt các tính năng như phát điện lên lưới.
* **Cấu trúc thiết bị có tổ chức:** (từ v0.2.0+) Các thực thể được tự động nhóm vào các thiết bị con hợp lý (PV, Lưới điện, EPS, Máy phát, Pin) để dễ quản lý trong Home Assistant.
* **Trạng thái chi tiết:** Một sensor văn bản dễ hiểu cho biết chính xác biến tần đang làm gì (ví dụ: "PV cấp tải & sạc pin").
* **Sensor tính toán:** Bao gồm các sensor suy ra như "Tỷ lệ tải" để có cái nhìn rõ hơn về hiệu suất hệ thống.
* **Polling cục bộ:** Toàn bộ giao tiếp diễn ra cục bộ. Không phụ thuộc cloud.

### Yêu cầu

Dongle ghi dữ liệu WiFi của biến tần LuxPower phải được kết nối vào cùng mạng cục bộ với Home Assistant. Bạn cần biết địa chỉ IP của nó.

### HACS (Home Assistant Community Store)

Tích hợp này có sẵn trong repository mặc định của HACS.

1.  Vào **HACS** > **Integrations** trong Home Assistant.
2.  Nhấn nút **Explore & Download Repositories**.
3.  Tìm "Luxpower Inverter (Modbus)" và nhấn **"Download"**.
4.  Khởi động lại Home Assistant khi được yêu cầu.

### Cài đặt thủ công

1.  Sao chép thư mục `lxp_modbus` từ repository này vào thư mục `custom_components` của Home Assistant.
2.  Khởi động lại Home Assistant.

## Cấu hình

Việc cấu hình được thực hiện hoàn toàn qua giao diện Home Assistant.

1.  Vào **Settings** > **Devices & Services**.
2.  Nhấn **Add Integration** và tìm **"Luxpower Inverter (Modbus)"**.
3.  Điền các thông tin yêu cầu cho biến tần của bạn.

### Các tùy chọn cấu hình

| Tên | Loại | Mô tả |
| :--- | :--- | :--- |
| **IP Address** | string | **(Bắt buộc)** Địa chỉ IP của dongle WiFi trên biến tần. |
| **Port** | integer | **(Bắt buộc)** Cổng giao tiếp cho kết nối Modbus, thường là `8000`. |
| **Dongle Serial Number**| string | **(Bắt buộc)** Số serial gồm 10 ký tự của dongle WiFi. |
| **Inverter Serial Number**| string | **(Bắt buộc)** Số serial gồm 10 ký tự của biến tần. |
| **Polling Interval** | integer | **(Bắt buộc)** Khoảng thời gian (giây) để truy vấn dữ liệu từ biến tần. Mặc định là 60. |
| **Inverter Rated Power**| integer | **(Bắt buộc)** Công suất định mức của biến tần tính bằng Watt (ví dụ `5000` cho biến tần 5kW). |
| **Entity Prefix** | string | (Tùy chọn) Tiền tố tùy chỉnh cho tên tất cả thực thể (ví dụ 'LXP'). Để trống nếu không cần tiền tố. |
| **Read-Only Mode** | boolean| (Tùy chọn) Xem cảnh báo quan trọng dưới đây trước khi thay đổi thiết lập này. |
| **Register Block Size** | integer | (Tùy chọn) Kích thước khối register khi đọc dữ liệu. Dùng `125` (mặc định) cho hầu hết biến tần, dùng `40` cho firmware cũ không hỗ trợ khối lớn hơn. |
| **Connection Retry Attempts** | integer | Số lần thử kết nối lại trước khi từ bỏ (mặc định là 3). |
| **Enable Device Grouping** | boolean | (từ v0.2.0+) Nhóm các thực thể vào thiết bị con hợp lý để dễ quản lý (mặc định: bật). |
| **Battery Entities** | string | (từ v1.0.0+) Cấu hình giám sát pin: `none` (tắt), `auto` (tự động phát hiện), hoặc danh sách số serial pin phân tách bằng dấu phẩy. |

> [!WARNING]
> ### Lưu ý quan trọng về Read-Only Mode (Có từ v0.1.5)
>
> Thiết lập **Read-Only Mode** thay đổi căn bản loại thực thể mà tích hợp này tạo ra cho các thiết lập điều khiển biến tần.
>
> * **Nếu `Read-Only Mode` TẮT (mặc định):** Tích hợp sẽ tạo các thực thể tương tác như `number`, `switch`, và `select` để bạn điều khiển biến tần.
> * **Nếu `Read-Only Mode` BẬT:** Tất cả các thực thể điều khiển đó sẽ được tạo thành thực thể `sensor` chỉ đọc. Bạn sẽ thấy được các thiết lập hiện tại nhưng không thể thay đổi.
>
> **Hãy lựa chọn thiết lập này thật kỹ ngay từ lần cài đặt đầu tiên.** Việc thay đổi tùy chọn này sau bằng cách cấu hình lại tích hợp sẽ **xóa** các thực thể điều khiển hiện có và tạo ra thực thể `sensor` mới (hoặc ngược lại). Điều này sẽ làm hỏng mọi dashboard, automation, hoặc lịch sử dữ liệu đang phụ thuộc vào các thực thể cũ.

> [!TIP]
> ### Cấu hình kích thước khối Register (Register Block Size)
>
> Tùy chọn **Register Block Size** cho phép bạn điều chỉnh cách tích hợp giao tiếp với biến tần:
>
> * **125** (Mặc định): Dùng cho hầu hết các phiên bản firmware biến tần hiện đại để có hiệu suất tốt nhất.
> * **40**: Dùng nếu biến tần của bạn có firmware cũ không hỗ trợ đọc khối register lớn.
>
> Nếu gặp lỗi giao tiếp với thiết lập mặc định, hãy thử chuyển sang kích thước khối nhỏ hơn.

> [!TIP]
> ### Cơ chế kết nối lại & độ tin cậy
>
> Tích hợp này bao gồm cơ chế kết nối lại nâng cao để xử lý các vấn đề tạm thời về mạng hoặc giao tiếp với biến tần:
>
> * **Connection Retry Attempts**: Cấu hình số lần tích hợp thử kết nối lại ngay khi kết nối thất bại (mặc định: 3).
> * **Tự động phục hồi**: Nếu mất kết nối, tích hợp sẽ tạm thời dùng dữ liệu đã lưu trong cache trong khi cố gắng kết nối lại.
> * **Polling thích ứng**: Trong quá trình phục hồi, tần suất polling sẽ tự động điều chỉnh để cân bằng giữa việc kết nối lại nhanh và giảm tải mạng.
> * **Giảm cấp nhẹ nhàng (Graceful Degradation)**: Các thực thể vẫn giữ giá trị hợp lệ cuối cùng trong thời gian gián đoạn kết nối ngắn.
>
> Các tính năng này giúp đảm bảo sự cố mạng tạm thời không làm hỏng automation hoặc khiến thực thể hiển thị "không khả dụng".

> [!IMPORTANT]
> ### Nhóm thiết bị (Device Grouping) (Có từ v0.2.0)
>
> Bắt đầu từ phiên bản 0.2.0, tích hợp này có tính năng **Nhóm thiết bị** để tổ chức tốt hơn hơn 250 thực thể được tạo ra từ biến tần:
>
> * **Nhóm PV** (25 thực thể): Giám sát pin mặt trời và điều khiển MPPT
> * **Nhóm Lưới điện** (42 thực thể): Kết nối lưới điện và dữ liệu nhập/xuất
> * **Nhóm EPS** (18 thực thể): Nguồn điện dự phòng / đầu ra tải khi mất điện
> * **Nhóm Máy phát** (12 thực thể): Giám sát và điều khiển máy phát dự phòng
> * **Nhóm Pin** (62 thực thể): Dữ liệu BMS, điện áp cell, nhiệt độ, và điều khiển pin
>
> **Tùy chọn cấu hình:**
> * **Bật theo mặc định** cho các bản cài mới - giúp tổ chức tốt hơn trong Home Assistant
> * **Tùy chọn** - có thể tắt trong thiết lập tích hợp nếu bạn muốn tất cả thực thể nằm dưới một thiết bị duy nhất
> * **Có thể cấu hình** - có thể bật/tắt bất kỳ lúc nào qua tùy chọn tích hợp

> [!TIP]
> ### Giám sát Pin (chỉ pin LXP) (Có từ v1.0.0)
>
> Bắt đầu từ phiên bản 1.0.0, tích hợp này có thể đọc dữ liệu pin trực tiếp từ BMS qua dải register Modbus 5000+. Mỗi pin cung cấp 18 sensor, bao gồm:
>
> * **Trạng thái:** SOC, SOH, Điện áp, Dòng điện, Dung lượng, Số chu kỳ
> * **Chi tiết Cell:** Điện áp cell Max/Min, Nhiệt độ cell Max/Min, Chênh lệch điện áp cell
> * **Chẩn đoán:** Phiên bản firmware, Dòng sạc/xả tối đa
>
> **Tùy chọn cấu hình:**
> * **`none`** (mặc định): Giám sát pin bị tắt.
> * **`auto`**: Tự động phát hiện các pin đang kết nối và tạo thực thể tương ứng.
> * **Danh sách số serial phân tách bằng dấu phẩy** (ví dụ `SN1234567890,SN0987654321`): Chỉ định thủ công những pin cần giám sát.
>
> Khi Nhóm thiết bị được bật, mỗi pin sẽ xuất hiện như một thiết bị con riêng dưới biến tần chính để dễ điều hướng.
>
> **Yêu cầu:** Polling dữ liệu pin yêu cầu Register Block Size ít nhất là 120. Nếu block size đặt là 40 (firmware cũ), giám sát pin sẽ không khả dụng.

## Các thực thể

Tích hợp này tạo ra rất nhiều thực thể để bạn có toàn quyền theo dõi và điều khiển biến tần.

#### Sensors
Cung cấp dữ liệu vận hành chi tiết, bao gồm:
* Trạng thái biến tần (Văn bản và Mã)
* SOC & SOH pin
* Công suất PV (tổng và theo từng chuỗi)
* Công suất nhập/xuất lưới điện
* Công suất tải
* Công suất sạc/xả pin
* Thống kê năng lượng theo ngày & tổng (PV, Lưới, Tải, v.v.)
* Nhiệt độ (Pin, Tản nhiệt, v.v.)
* Điện áp, Dòng điện và Tần số cho Lưới điện, EPS, và Pin.
* Tỷ lệ tải được tính toán

#### Numbers
Cho phép điều khiển các thiết lập của biến tần:
* Dòng sạc & xả
* Giới hạn công suất sạc AC
* SOC dừng xả (EOD)
* Điện áp/SOC dừng sạc pin

#### Switches
Bật hoặc tắt các tính năng chính ngay lập tức:
* Bật sạc AC
* Bật phát lên lưới
* Bật xả cưỡng bức
* Chế độ Eco & Green

#### Selects
Chọn từ các chế độ vận hành định sẵn:
* Kiểu sạc AC (theo thời gian, SOC, v.v.)
* Ưu tiên đầu ra (Ưu tiên pin, ưu tiên PV, v.v.)

#### Time
Đặt lịch cho các hoạt động theo thời gian:
* Giờ bắt đầu & kết thúc sạc AC
* Giờ bắt đầu & kết thúc cắt đỉnh tải

## Blueprint

Tích hợp này bao gồm các blueprint giúp bạn bắt đầu nhanh với các automation mạnh mẽ.

### Cách import Blueprint

Có hai cách để đưa blueprint vào Home Assistant của bạn.

**Cách 1: Nút Import trực tiếp (Dễ nhất)**

Nhấn nút "Import Blueprint" dưới blueprint bạn muốn dùng. Bạn sẽ được chuyển đến Home Assistant để hoàn tất việc import.

**Cách 2: Import thủ công**

1.  Trong Home Assistant, vào **Settings** > **Automations & Scenes**.
2.  Chọn tab **Blueprints**.
3.  Nhấn nút **Import Blueprint** ở góc dưới bên phải.
4.  Dán "Manual Import URL" của blueprint bạn muốn.
5.  Nhấn **"Preview Blueprint"** sau đó **"Import Blueprint"**.

---

### Các Blueprint hiện có

#### Sạc cưỡng bức trong khoảng thời gian xác định
Blueprint script này cho phép bạn tạm thời buộc biến tần sạc từ lưới điện trong một khoảng thời gian xác định. Nó sẽ lưu lại các thiết lập hiện tại, áp dụng lịch sạc tạm thời, và khôi phục lại thiết lập cũ khi hoàn tất.

[![Open your Home Assistant instance and import this blueprint.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fant0nkr%2Fluxpower-ha-integration%2Fmain%2Fblueprints%2Fscript%2Flxp_force_charge.yaml)
> Manual Import URL: `https://raw.githubusercontent.com/ant0nkr/luxpower-ha-integration/main/blueprints/script/lxp_force_charge.yaml`

#### Sạc cưỡng bức đến mức SOC mục tiêu
Blueprint automation này cho phép bạn sạc pin biến tần từ lưới AC cho đến khi đạt đến mức SOC (trạng thái sạc) mục tiêu. Nó tự động lưu lại bản sao các thiết lập hiện tại trước khi bắt đầu, và khôi phục lại hoàn hảo khi đạt được SOC mục tiêu.

[![Open your Home-Assistant instance and import this blueprint.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fant0nkr%2Fluxpower-ha-integration%2Fmain%2Fblueprints%2Fautomation%2Flxp_charge_automation.yaml)
> Manual Import URL: `https://raw.githubusercontent.com/ant0nkr/luxpower-ha-integration/main/blueprints/automation/lxp_charge_automation.yaml`

## Gỡ lỗi (Debugging)

Nếu bạn gặp vấn đề, có thể bật ghi log debug bằng cách thêm dòng sau vào file `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.lxp_modbus: debug
```
